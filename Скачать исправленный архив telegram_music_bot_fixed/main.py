import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7239702640:AAHu_THwSc4VqADqKYgCc5fXJ0o-etTMAsA"

# === Загрузка песни ===
async def download_and_send_song(query, update):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            filename = ydl.prepare_filename(info['entries'][0]).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            title = info['entries'][0]['title']

            await update.message.reply_audio(audio=open(filename, 'rb'), title=title)
            os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"Ошибка при загрузке песни 😔\n{e}")

# === Обработка команды /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши название песни, и я пришлю тебе mp3 🎶")

# === Обработка текста ===
async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("Ищу песню... ⏳")
    await download_and_send_song(query, update)

# === Запуск бота ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))
    app.run_polling()
