import urllib.request, json, time, threading
from datetime import datetime, timedelta
from flask import Flask
import os

TOKEN = os.environ.get("TOKEN", "").strip()
CHAT_ID = os.environ.get("CHAT_ID", "8698451791")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def send(msg):
    for i in range(3):
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            data = {"chat_id": CHAT_ID, "text": msg}
            req = urllib.request.Request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req, timeout=15)
            print("Sent OK")
            return True
        except Exception as e:
            print(f"Retry {i+1} - {e}")
            time.sleep(5)
    return False

def get_binance(symbol):
    for base in ["https://api.binance.com", "https://api.binance.us"]:
        try:
            url = f"{base}/api/v3/ticker/price?symbol={symbol}"
            d = json.loads(urllib.request.urlopen(url, timeout=15).read().decode())
            return float(d['price'])
        except:
            continue
    return None

def get_forex():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        d = json.loads(urllib.request.urlopen(url, timeout=15).read().decode())
        r = d['rates']
        eurusd = 1 / r['EUR']; gbpusd = 1 / r['GBP']; audusd = 1 / r['AUD']; nzdusd = 1 / r['NZD']
        usdjpy = r['JPY']; usdchf = r['CHF']; usdcad = r['CAD']
        return {
            "EURUSD": eurusd, "GBPUSD": gbpusd, "AUDUSD": audusd, "NZDUSD": nzdusd,
            "USDJPY": usdjpy, "USDCHF": usdchf, "USDCAD": usdcad,
            "EURJPY": eurusd * usdjpy, "GBPJPY": gbpusd * usdjpy, "AUDJPY": audusd * usdjpy,
            "NZDJPY": nzdusd * usdjpy, "EURGBP": eurusd / gbpusd, "EURCHF": eurusd * usdchf,
            "GBPCHF": gbpusd * usdchf, "EURAUD": eurusd / audusd, "GBPAUD": gbpusd / audusd,
            "AUDCAD": audusd * usdcad, "EURCAD": eurusd * usdcad, "GBPCAD": gbpusd * usdcad,
            "NZDCHF": nzdusd * usdchf,
        }
    except Exception as e:
        print(f"Forex fail {e}")
        return {}

PAIRS = {
    "PAXGUSDT": ("XAUUSD - ذهب", 1.5, 8, 8),
    "XAGUSDT": ("XAGUSD - فضة", 0.05, 0.25, 0.25),
    "BTCUSDT": ("BTC - بيتكوين", 80, 300, 300),
    "ETHUSDT": ("ETH - ايثيريوم", 8, 30, 30),
    "SOLUSDT": ("SOL - سولانا", 1.0, 4, 4),
    "EURUSD": ("EURUSD - يورو", 0.0008, 0.0020, 0.0020),
    "GBPUSD": ("GBPUSD - باوند", 0.0008, 0.0020, 0.0020),
    "USDJPY": ("USDJPY - ين", 0.08, 0.25, 0.25),
    "USDCHF": ("USDCHF - فرنك", 0.0008, 0.0020, 0.0020),
    "USDCAD": ("USDCAD - كندي", 0.0008, 0.0020, 0.0020),
    "AUDUSD": ("AUDUSD - استرالي", 0.0008, 0.0020, 0.0020),
    "NZDUSD": ("NZDUSD - نيوزلندي", 0.0008, 0.0020, 0.0020),
    "EURJPY": ("EURJPY - يورو ين", 0.08, 0.25, 0.25),
    "GBPJPY": ("GBPJPY - باوند ين", 0.10, 0.30, 0.30),
    "AUDJPY": ("AUDJPY - استرالي ين", 0.08, 0.25, 0.25),
    "NZDJPY": ("NZDJPY - نيوزلندي ين", 0.08, 0.25, 0.25),
    "EURGBP": ("EURGBP - يورو باوند", 0.0006, 0.0015, 0.0015),
    "EURCHF": ("EURCHF - يورو فرنك", 0.0008, 0.0020, 0.0020),
    "GBPCHF": ("GBPCHF - باوند فرنك", 0.0008, 0.0020, 0.0020),
    "EURAUD": ("EURAUD - يورو استرالي", 0.0008, 0.0020, 0.0020),
    "GBPAUD": ("GBPAUD - باوند استرالي", 0.0008, 0.0020, 0.0020),
    "AUDCAD": ("AUDCAD - استرالي كندي", 0.0008, 0.0020, 0.0020),
    "EURCAD": ("EURCAD - يورو كندي", 0.0008, 0.0020, 0.0020),
    "GBPCAD": ("GBPCAD - باوند كندي", 0.0008, 0.0020, 0.0020),
    "NZDCHF": ("NZDCHF - نيوزلندي فرنك", 0.0006, 0.0015, 0.0015),
}

def run_bot():
    send("BOT PRO MAX ON - Server 24h - 5 Min")
    last = {}
    for sym in ["PAXGUSDT","XAGUSDT","BTCUSDT","ETHUSDT","SOLUSDT"]:
        p = get_binance(sym)
        if p: last[sym] = p
    for k,v in get_forex().items():
        if k in PAIRS: last[k] = v
    print(f"Start pairs: {len(last)}")
    while True:
        try:
            time.sleep(300)
            now = datetime.now()
            entry_time = now.strftime("%H:%M:%S")
            close_time = (now + timedelta(minutes=5)).strftime("%H:%M:%S")
            current = {}
            for sym in ["PAXGUSDT","XAGUSDT","BTCUSDT","ETHUSDT","SOLUSDT"]:
                p = get_binance(sym)
                if p: current[sym] = p
            for k,v in get_forex().items():
                if k in PAIRS: current[k] = v
            for sym, price in current.items():
                if sym not in last:
                    last[sym] = price
                    continue
                name, thresh, tp_val, sl_val = PAIRS[sym]
                diff = price - last[sym]
                if abs(diff) > thresh:
                    if diff > 0:
                        tp = price + tp_val; sl = price - sl_val
                        msg = f"""🟢 {name} - CALL / اخضر\n💰 سعر الدخول: {price:,.4f}\n🎯 الهدف TP: {tp:,.4f}\n🛑 الستوب SL: {sl:,.4f}\n⏰ وقت الدخول: {entry_time}\n⏰ وقت الاغلاق: {close_time}\n⏳ المدة: 5 دقائق\n📈 الاتجاه: صاعد\n✅ اذا قال CALL / اخضر -> ادخل صفقة شراء 5 دقائق في نفس وقت الدخول\n⚠️ لا تدخل اذا تأخرت اكثر من 1 دقيقة عن وقت الدخول"""
                    else:
                        tp = price - tp_val; sl = price + sl_val
                        msg = f"""🔴 {name} - PUT / احمر\n💰 سعر الدخول: {price:,.4f}\n🎯 الهدف TP: {tp:,.4f}\n🛑 الستوب SL: {sl:,.4f}\n⏰ وقت الدخول: {entry_time}\n⏰ وقت الاغلاق: {close_time}\n⏳ المدة: 5 دقائق\n📉 الاتجاه: هابط\n✅ اذا قال PUT / احمر -> ادخل صفقة بيع 5 دقائق في نفس وقت الدخول\n⚠️ لا تدخل اذا تأخرت اكثر من 1 دقيقة عن وقت الدخول"""
                    send(msg)
                    print(f"Signal {name} {price}")
                else:
                    print(f"No signal {name}")
                last[sym] = price
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(10)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
