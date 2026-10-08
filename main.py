import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler , MessageHandler, filters, ConversationHandler
from telegram import Update
from functions import memorizing
from telegram.error import TelegramError

load_dotenv()
BOT_TOKEN =os.environ["TELEGRAM_TOKEN"]
FOLDER=0
# START -----------------
async def start(update: Update, context):
    await update.message.reply_text(
        "Hello! I'm Sinabro, your friendly bot!\nI'm always ready to receive your files!"
    )
# HELP ------------------
async def help_command(update: Update, context):
    await update.message.reply_text(
        "I can help you keep your files organised! "
        "Just send me a file and I'll save it in the right folder.\n/delete : to remove file from folder\n/move : to change your file location"
    )


async def receive_file(update: Update, context):
    document = update.message.document
    context.user_data["file_id"] = document.file_id
    context.user_data["file_name"] = document.file_name
    await update.message.reply_text("Which folder should I put it in? (/cancel to stop)")
    return FOLDER

async def receive_folder(update: Update, context):
    folder_name = update.message.text.strip()
    file_name= context.user_data["file_name"]
    try:
        saved = await memorizing(update, context)
    except (TelegramError, OSError):
        
        saved = False
        await update.message.reply_text(
            "I couldn't save the file (it may be over 20 MB, or the folder name isn't valid)."
        )

    if saved:
        await update.message.reply_text(f"Saved {file_name} in {folder_name}!!!")
    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text("Your order has been cancelled.")
    return ConversationHandler.END



conversazione=ConversationHandler(
    entry_points=[MessageHandler(filters.Document.ALL, receive_file)],
    states={
        FOLDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_folder)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]

)



bot = Application.builder().token(BOT_TOKEN).build()

bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("help", help_command))
bot.add_handler(conversazione)




bot.run_polling()

