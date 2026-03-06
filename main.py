from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes
from dotenv import load_dotenv
import os
import datetime
from agents.summmary_agent import Summary_agent
from agents.sorting import Sorting_agent
from tools.fetch_news import Genrate_topic
from llm.llm import FutureScope_Bot
import datetime
from datetime import timedelta
import pytz
load_dotenv()

token=os.getenv('Token')
username=os.getenv('UserName')
model_key=os.getenv('OPENROUTER_KEY')
Subscriber=set()
# Summary_agent(topics)
now = datetime.datetime.now()
print("Current time:", now)
def split_message(text, chunk_size=4000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
print("Subscriber is ",Subscriber)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    Subscriber.add(update.effective_user.id)
    await update.message.reply_text("🤖 You are subscribed to AI News!\n"
        "You will receive updates:\n"
        "🌅 Morning\n☀️ Afternoon\n🌙 Night")
    print(Subscriber)
    
async def news(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Bot Try Fetch News🔍....')
    genrate_news=Genrate_topic().genrate_topic_api()

    await update.message.reply_text('Bot Try Fetch Topic🔍....')
    summary_data=Summary_agent(genrate_news).summary

    await update.message.reply_text('Bot Try Fetch Summary....')
    sorted_data=Sorting_agent().sorting_data(summary_data)

    await update.message.reply_text('Bot Try Fetch Sorted....')
    
    await update.message.reply_text(sorted_data)
    await update.message.reply_text('End Fetch News🔍....')

async def send_news(context:ContextTypes.DEFAULT_TYPE):
    print("Run at Time.................")
    print("Job Que is Run")
    if not Subscriber:
        return
    # await update.message.reply_text('Bot Try Fetch News🔍....')
    genrate_news=Genrate_topic().genrate_topic_api()

    # await update.message.reply_text('Bot Try Fetch Topic🔍....')
    summary_data=Summary_agent(genrate_news).summary

    # await update.message.reply_text('Bot Try Fetch Summary....')
    sorted_data=Sorting_agent().sorting_data(summary_data)

    # await update.message.reply_text('Bot Try Fetch Sorted....')

    print("Sending news to:", Subscriber)
    for sub_id in Subscriber:
        if len(sorted_data)>4000:
            for i in range(0,len(sorted_data),4000):
                await context.bot.send_message(chat_id=sub_id,text=sorted_data[i:i+4000])
        else:
            await context.bot.send_message(chat_id=sub_id,text=sorted_data)

async def echo(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_input=update.message.text
    await update.message.reply_text(f"user said {user_input}")

async def llm_query_handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
    FB=FutureScope_Bot("meta-llama/llama-3-8b-instruct",temp=0.5,model_key=model_key)
    await update.message.reply_text(f"Thinking")
    result=FB.input(update.message.text) 
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
    job_queue.run_daily(
        send_news,
        time=datetime.time(hour=9, minute=0)
    )

    # Afternoon 2 PM
    job_queue.run_daily(
        send_news,
        time=datetime.time(hour=14, minute=0)
    )

    # Night 11:25 PM
    job_queue.run_daily(
        send_news,
        time=datetime.time(hour=23, minute=25)
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