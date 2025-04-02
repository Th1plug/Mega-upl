
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from mega import Mega

TOKEN = "7629171030:AAEcKcOINU6x1Kg_AT5_vuDjIpY_wTtCNGI"
UPLOADER_BOT_USERNAME = "@urluploaderbot"

mega = Mega()
video_links = []
waiting = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Stuur een MEGA folder link. Ik stuur de video's één voor één naar de uploaderbot.")

async def handle_mega(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global video_links, waiting

    text = update.message.text.strip()
    if "mega.nz" not in text:
        return

    await update.message.reply_text("Bezig met ophalen van video's...")
    try:
        m = mega.login()
        folder = m._parse_url(text)
        files = m.get_public_url_files(folder)
    except Exception as e:
        await update.message.reply_text(f"Fout bij ophalen: {e}")
        return

    video_links = [f['link'] for f in files if f['name'].lower().endswith(('.mp4', '.mkv', '.avi'))]

    if not video_links:
        await update.message.reply_text("Geen video's gevonden.")
        return

    await update.message.reply_text(f"{len(video_links)} video's gevonden. Versturen begint...")
    waiting = True
    await context.bot.send_message(chat_id=UPLOADER_BOT_USERNAME, text=video_links.pop(0))

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting, video_links

    if not waiting:
        return
    if update.message.chat.username != UPLOADER_BOT_USERNAME.lstrip("@"):
        return
    if update.message.video or update.message.document or update.message.photo:
        if video_links:
            await context.bot.send_message(chat_id=UPLOADER_BOT_USERNAME, text=video_links.pop(0))
        else:
            waiting = False
            await context.bot.send_message(chat_id=UPLOADER_BOT_USERNAME, text="Klaar!")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("mega.nz"), handle_mega))
    app.add_handler(MessageHandler(filters.ALL, handle_response))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
