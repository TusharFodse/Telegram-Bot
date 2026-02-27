from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes
from dotenv import load_dotenv
import os
load_dotenv()

token=os.getenv('Token')
username=os.getenv('UserName')

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is Start 🤖....")
async def echo(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_input=update.message.text
    await update.message.reply_text(f"user said {user_input}")


app=ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,echo))
print("BOT is Running..........")
app.run_polling()