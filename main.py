import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler , MessageHandler, filters, ConversationHandler
from telegram import Update

load_dotenv()
BOT_TOKEN =os.environ["TELEGRAM_TOKEN"]
FOLDER=0

async def start(update: Update, context):
    await update.message.reply_text(
        "Hello! I'm Sinabro, your friendly bot!\nI'm ready to receive your files!"
    )

async def help_command(update: Update, context):
    await update.message.reply_text(
        "I can help you keep your files organised! "
        "Just send me a file and I'll save it in the right folder."
    )

async def show_id(update: Update, context):
    await update.message.reply_text(f"Il tuo ID è {update.effective_user.id}")

async def receive_file(update: Update, context):
    document = update.message.document
    context.user_data["file_id"] = document.file_id
    context.user_data["file_name"] = document.file_name
    await update.message.reply_text("Which folder should I put it in? (/cancel to stop)")
    return FOLDER

async def receive_folder(update: Update, context):
    folder = update.message.text
    file_name = context.user_data["file_name"]
    await update.message.reply_text(f"I'll save {file_name} in {folder}")
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context):
    context.user_data.clear()
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END



conversazione=ConversationHandler(
    entry_points=[MessageHandler(filters.Document.ALL, receive_file)],
    states={
        FOLDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_folder)],
    }
    fallbacks=[CommandHandler("cancel", cancel)]

)



bot = Application.builder().token(BOT_TOKEN).build()

bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("help", help_command))
bot.add_handler(CommandHandler("id", show_id))
bot.add_handler(conversazione)



# start and poll for updates, press CRTL+C to stop
bot.run_polling()

