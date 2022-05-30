from Classes import Bot
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")


bot = Bot(api_key=api_key, secret_key=secret_key, balance=75, timeframe="1m", sma=10)


try:
    bot.run_bullish_engulfing()
except:
    bot.run_bullish_engulfing()
