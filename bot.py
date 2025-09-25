import yfinance as yf
import talib
import pandas as pd
import schedule, time
from telegram import Bot
import datetime

BOT_TOKEN = "your_bot_token"        # 🔹 Replace with your token
CHANNEL_ID = "@Trade_clusterbot"   # 🔹 Replace with your channel username
bot = Bot(token=BOT_TOKEN)

stocks = ["RELIANCE.NS", "HDFCBANK.NS", "INFY.NS", "TCS.NS"]  # Example

def get_intraday_picks():
    picks = []
    for s in stocks:
        try:
            data = yf.download(s, interval="5m", period="5d")
            close = data["Close"]

            ema20 = talib.EMA(close, timeperiod=20)
            rsi = talib.RSI(close, timeperiod=14)

            latest_price = close.iloc[-1]
            latest_ema20 = ema20.iloc[-1]
            latest_rsi = rsi.iloc[-1]

            if latest_price > latest_ema20 and 45 < latest_rsi < 65:
                picks.append(s.replace(".NS", ""))
        except Exception as e:
            print(f"Error for {s}: {e}")
    return picks

def send_daily_update():
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    picks = get_intraday_picks()
    
    if not picks:
        message = f"📊 Intraday Picks for {today}\n\n⚠️ No suitable stocks found today."
    else:
        message = f"📊 Intraday Picks for {today}\n\n"
        for stock in picks:
            message += f"✅ {stock}\n"
    
    bot.send_message(chat_id=CHANNEL_ID, text=message)

schedule.every().day.at("09:15").do(send_daily_update)

print("🔄 Bot is running on Railway...")

while True:
    schedule.run_pending()
    time.sleep(30)
