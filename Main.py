import os
import telebot
import yt_dlp
import threading
from flask import Flask

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8411260158:AAGz5pH7mQ6LwYgJ9zV0qK1e1b9t8R0eX5yZ")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "-1000000000000")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "BOT IS LIVE"

def download_video(url):
    ydl_opts = {'format': 'best[ext=mp4]/best','outtmpl': '%(title)s.%(ext)s','noplaylist': True,'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename, info.get('title', 'Video')
    except Exception as e:
        return None, str(e)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalam-o-Alaikum! Link bhejo")

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    url = message.text.strip()
    if "http" not in url:
        return
    bot.reply_to(message, "Downloading...")
    file_path, title = download_video(url)
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                bot.send_video(message.chat.id, f, caption=title)
            os.remove(file_path)
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
    else:
        bot.reply_to(message, f"Failed: {title}")

def run_bot():
    print("BOT STARTED - Polling Active")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
