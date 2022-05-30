from Classes import Bot
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")


bot = Bot(api_key=api_key, secret_key=secret_key, balance=80, timeframe="1m")
# bot.run_bullish_engulfing()
# get_all_orders(bot.clientFutures)
try:
    bot.run_bullish_engulfing()
except:
    bot.run_bullish_engulfing()
