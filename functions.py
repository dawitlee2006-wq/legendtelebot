import os
from pathlib import Path
from telegram import Update

# Cartella dentro cui finiscono tutte le sottocartelle
BASE_FOLDER = Path("files").resolve()


async def memorizing(update: Update, context) -> bool:
    # Solo il proprietario può salvare file (il valore di .env è testo, va convertito)
    if int(os.environ["OWNERTELE_ID"]) != update.effective_user.id:
        await update.message.reply_text("You are not allowed to use this bot!")
        return False

    folder = update.message.text.strip()
    # .name tiene solo il nome del file, scartando eventuali percorsi
    file_name = Path(context.user_data["file_name"] or "unnamed_file").name
    destination = (BASE_FOLDER / folder / file_name).resolve()

    # Impedisce di scrivere fuori dalla cartella base (es. "../..")
    if not destination.is_relative_to(BASE_FOLDER):
        await update.message.reply_text("That folder name is not valid.")
        return False

    # Crea la cartella se non esiste, poi scarica il file da Telegram
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = await context.bot.get_file(context.user_data["file_id"])
    await document.download_to_drive(destination)
    return True