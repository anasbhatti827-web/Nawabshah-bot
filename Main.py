import os
import threading
from flask import Flask
import telebot
import time
from datetime import datetime
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Aapka Channel ya Group ID yahan se ayega - Environment me add kiya hua
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1000000000000")

@app.route('/')
def home():
    return "Nawabshah Bot is Live! Bot Started"

def send_aviator_signal():
    try:
        now = datetime.now(pytz.timezone('Asia/Kar
