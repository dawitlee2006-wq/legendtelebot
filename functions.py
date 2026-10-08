import os
from pathlib import Path
from telegram import Update


BASE_FOLDER = (Path.home() / "Desktop" / "filetelegram").resolve()


async def memorizing(update: Update, context) -> bool:
    
    if os.environ["OWNERTELE_ID"] != str(update.effective_user.id):
        await update.message.reply_text("You are not allowed to use this bot!")
        return False

    folder = update.message.text.strip()
    
    file_name = Path(context.user_data["file_name"] or "unnamed_file").name
    destination = (BASE_FOLDER / folder / file_name).resolve()

    
    if not destination.is_relative_to(BASE_FOLDER):
        await update.message.reply_text("That folder name is not valid.")
        return False

    
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = await context.bot.get_file(context.user_data["file_id"])
    await document.download_to_drive(destination)
    return True