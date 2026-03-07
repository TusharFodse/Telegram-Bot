from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes
from dotenv import load_dotenv
import os
from agents.summmary_agent import Summary_agent
from agents.sorting import Sorting_agent
from tools.fetch_news import Genrate_topic
from llm.llm import FutureScope_Bot
import datetime
from datetime import timedelta
import pytz
import sqlite3
from tools.database import add_subscriber,get_subscriber,init_db

load_dotenv()
init_db()

last_fetch = None
cached_news = None
CACHE_DURATION = 1800

token=os.getenv('Token')
username=os.getenv('UserName')
model_key=os.getenv('OPENROUTER_KEY')

# Summary_agent(topics)
now = datetime.datetime.now()
print("Current time:", now)
FB=FutureScope_Bot("meta-llama/llama-3-8b-instruct",temp=0.5,model_key=model_key)
def split_message(text, chunk_size=4000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


     
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    add_subscriber(update.effective_user.id)
    await update.message.reply_text("🤖 You are subscribed to AI News!\n"
        "You will receive updates:\n"
        "🌅 Morning\n☀️ Afternoon\n🌙 Night")




async def news(update:Update,context:ContextTypes.DEFAULT_TYPE):
    global last_fetch,cached_news
    now=datetime.datetime.now()
    if cached_news and last_fetch:
        if (now-last_fetch).total_seconds() < CACHE_DURATION:
            print("Using cached news")
            if len(cached_news)>4000:
                for part in split_message(cached_news):
                    await update.message.reply_text(part)   
                return
            else:
                 await update.message.reply_text(cached_news)    
                 return
    await update.message.reply_text('Bot Try Fetch News🔍....')
    genrate_news=Genrate_topic().genrate_topic_api()
    summary_data=Summary_agent(genrate_news).summary
    sorted_data=Sorting_agent().sorting_data(summary_data)
    cached_news=sorted_data
    last_fetch=now 
    if len(sorted_data)>4000:    
        for part in split_message(sorted_data):
            await update.message.reply_text(part)
    else:
         await update.message.reply_text(sorted_data)
    return

async def send_news(context:ContextTypes.DEFAULT_TYPE):
    global last_fetch,cached_news
    print("Run at Time.................")
    print("Job Que is Run")
    now=datetime.datetime.now()
    all_user_id=get_subscriber()
    if cached_news and last_fetch:
        if(now-last_fetch).total_seconds() < CACHE_DURATION:
            sorted_data=cached_news
                
        else:
            # await update.message.reply_text('Bot Try Fetch News🔍....')
            genrate_news=Genrate_topic().genrate_topic_api()

            # await update.message.reply_text('Bot Try Fetch Topic🔍....')
            summary_data=Summary_agent(genrate_news).summary

            # await update.message.reply_text('Bot Try Fetch Summary....')
            sorted_data=Sorting_agent().sorting_data(summary_data)
            cached_news = sorted_data
            last_fetch = now
    else:        
        # await update.message.reply_text('Bot Try Fetch News🔍....')
        genrate_news=Genrate_topic().genrate_topic_api()
        # await update.message.reply_text('Bot Try Fetch Topic🔍....')
        summary_data=Summary_agent(genrate_news).summary
        # await update.message.reply_text('Bot Try Fetch Summary....')
        sorted_data=Sorting_agent().sorting_data(summary_data)
        cached_news = sorted_data
        last_fetch = now
        # await update.message.reply_text('Bot Try Fetch Sorted....')
        
    for user in all_user_id:

        if len(sorted_data)>4000:
                for i in range(0,len(sorted_data),4000):
                    try:
                        await context.bot.send_message(chat_id=user,text=sorted_data[i:i+4000])
                    except Exception as e:
                         print(f"Failed to send to {user}: {e}")   
        else:
                try:
                    await context.bot.send_message(chat_id=user,text=sorted_data)
                except Exception as e:
                     print(f"Failed to send to {user}: {e}")



async def llm_query_handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Thinking")
    result=FB.input(query=update.message.text) 
    await update.message.reply_text(result)
    
def main():
    app=ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start",start))
    # app.add_handler(CommandHandler("news",news))
    job_queue=app.job_queue
#     job_queue.run_daily(
#     send_news,
#     time=datetime.time(hour=23, minute=32, tzinfo=pytz.timezone("Asia/Kolkata"))
# )
    IST = pytz.timezone("Asia/Kolkata")

    job_queue.run_daily(
        send_news,
        time=datetime.time(hour=9, minute=0, tzinfo=IST)
    )

    job_queue.run_daily(
        send_news,
        time=datetime.time(hour=14, minute=0, tzinfo=IST)
    )

    job_queue.run_daily(
        send_news,
        time=datetime.time(hour=21, minute=0, tzinfo=IST)
    )
    

    # run_time = datetime.datetime.now() + timedelta(minutes=1)
    # print("Job Que is Run")
    # job_queue.run_once(
    #     send_news,
    #     when=run_time
    # )
    # app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,llm_query_handle))
    print("BOT is Running..........")
    app.run_polling()

if __name__=="__main__":
    main()