Sinabro

Sinabro è un bot Telegram che riceve file in chat e li salva sul computer, nella cartella scelta dall'utente.

Mandi un documento al bot, lui ti chiede in quale cartella metterlo, e il file viene scaricato in Desktop/filetelegram/<cartella>.

Come funziona
Invii un documento al bot.
Il bot risponde: "Which folder should I put it in?"
Scrivi il nome della cartella (per esempio fisica 2).
Il bot scarica il file da Telegram e lo salva in Desktop/filetelegram/fisica 2/. Se la cartella non esiste, viene creata.
Il bot conferma con "Saved ... in ...".

In qualsiasi momento puoi scrivere /cancel per annullare.

Comandi
Comando	Cosa fa
/start	Messaggio di benvenuto
/help	Spiega cosa sa fare il bot
/cancel	Annulla il salvataggio in corso

/delete e /move sono citati nell'help ma non sono ancora implementati.

Requisiti
Python 3.9 o successivo
python-telegram-bot versione 20 o successiva
python-dotenv
Installazione
Installa le librerie:
   pip install python-telegram-bot python-dotenv
Crea un bot su Telegram scrivendo a @BotFather e copia il token che ti fornisce.
Trova il tuo ID utente Telegram (per esempio con @userinfobot).
Nella cartella del progetto crea un file .env con questo contenuto:
   TELEGRAM_TOKEN=il_token_del_bot
   OWNERTELE_ID=il_tuo_id_numerico

Non condividere questo file e non caricarlo su GitHub: aggiungi .env al .gitignore.

Avvio
python main.py

Il bot resta in ascolto finché non lo fermi con CTRL+C. I file vengono salvati sul computer su cui gira lo script, quindi il bot funziona solo mentre il programma è in esecuzione.

Struttura del progetto
File	Contenuto
main.py	Avvio del bot, comandi /start e /help, conversazione per ricevere il file e la cartella
functions.py	Funzione memorizing: controlla l'utente, costruisce il percorso, scarica il file
.env	Token del bot e ID del proprietario (da creare, non incluso)
La conversazione

Il flusso è gestito da un ConversationHandler con un solo stato:

Ingresso: l'arrivo di un documento (receive_file). Il bot salva file_id e nome del file in context.user_data e passa allo stato FOLDER.
Stato FOLDER: il bot aspetta un messaggio di testo con il nome della cartella (receive_folder), poi chiama memorizing e chiude la conversazione.
Uscita di emergenza: /cancel.
Sicurezza
Solo il proprietario può salvare file. L'ID di chi scrive viene confrontato con OWNERTELE_ID; gli altri utenti ricevono "You are not allowed to use this bot!".
I file non possono uscire dalla cartella base. Il percorso di destinazione viene risolto e verificato: un nome di cartella che porta fuori da filetelegram (per esempio con ..) viene rifiutato.
Il nome del file viene ripulito, tenendo solo il nome ed eliminando eventuali percorsi al suo interno.
Cambiare la cartella di destinazione

La cartella base è definita in functions.py:

python
BASE_FOLDER = (Path.home() / "Desktop" / "filetelegram").resolve()

Modifica questa riga per salvare altrove. Su Windows con OneDrive attivo il desktop può trovarsi in OneDrive/Desktop: in quel caso aggiungi "OneDrive" prima di "Desktop".

Limiti attuali
Funziona solo con i file inviati come documento. Foto e video inviati normalmente vengono ignorati.
Telegram permette ai bot di scaricare file fino a 20 MB.
Un file con lo stesso nome nella stessa cartella sovrascrive quello esistente.
Un secondo file inviato mentre il bot aspetta il nome della cartella viene ignorato: rispondi prima con la cartella o con /cancel.
Lo stato della conversazione è in memoria e si perde al riavvio del bot.
Sviluppi previsti
Comando /delete per rimuovere un file da una cartella
Comando /move per spostare un file
Supporto per foto e video
Riorganizzazione del codice a plugin (corpo principale + un modulo per ogni funzionalità)