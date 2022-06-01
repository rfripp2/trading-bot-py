from msilib.schema import Error
from Classes import Bot
from dotenv import load_dotenv
import os
from binance_orders import *
from logger import logger
load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")


bot = Bot(api_key=api_key, secret_key=secret_key,
          balance=40, timeframe="1m", sma=10)


if __name__ == '__main__':
    try:
        bot.run_bullish_engulfing()
        bot.stream_account_trades()
        logger.info("Bot and stream orders running")

    except Error:
        bot.run_bullish_engulfing()
        bot.stream_account_trades()
        logger.error("CRITICAL ERROR:", Error)
