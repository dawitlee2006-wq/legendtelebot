import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler , MessageHandler, filters
from telegram import Update

load_dotenv()
BOT_TOKEN =os.environ["TELEGRAM_TOKEN"]

async def start(update: Update):
    await update.message.reply_text(
        "Hello! I'm Sinabro, your friendly bot!\nI'm ready to receive your files!"
    )

async def help_command(update: Update):
    await update.message.reply_text(
        "I can help you keep your files organised! "
        "Just send me a file and I'll save it in the right folder."
    )

async def show_id(update: Update):
    await update.message.reply_text(f"Il tuo ID è {update.effective_user.id}")




bot = Application.builder().token(BOT_TOKEN).build()

bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("help", help_command))
bot.add_handler(CommandHandler("id", show_id))



# start and poll for updates, press CRTL+C to stop
bot.run_polling()

