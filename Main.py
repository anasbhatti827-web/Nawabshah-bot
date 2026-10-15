from flask import Flask
import urllib.request, json, time, threading, os

BOT_TOKEN = "8965657584:AAHJM3RhF5LFFL0a8nc-51RvzeqjSkVHYC0"
CHAT_ID = "8651497769"

app = Flask(__name__)

def get_signal():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=20"
    with urllib.request.urlopen(url, timeout=15) as r:
        data = json.loads(r.read().decode())
        closes = [float(x[4]) for x in data]
        price = closes[-1]
        avg = sum(closes[-10:]) / 10
        return ("BUY" if price > avg else "SELL"), price

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
    urllib.request.urlopen(req, timeout=15)

def bot_loop():
    while True:
        try:
            side, price = get_signal()
            if side == "BUY":
                msg = f"🚀🚀🚀 ادھر BUY کر لو 🚀🚀🚀\n\nCoin: BTCUSDT\nEntry: ${price:.2f}\nTime: 5min Signal"
            else:
                msg = f"🔻🔻🔻 ادھر SELL کر دو 🔻🔻🔻\n\nCoin: BTCUSDT\nEntry: ${price:.2f}\nTime: 5min Signal"
            send_msg(msg)
        except Exception as e:
            print(e)
        time.sleep(300)

@app.route('/')
def home():
    return "Bot is Running 24 Hours!"

threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
