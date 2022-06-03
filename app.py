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
          balance=40, timeframe="1m", sma=2)


if __name__ == '__main__':
    try:
        bot.run_bullish_engulfing()
        logger.info("Bot running")

    except Error:
        bot.run_bullish_engulfing()
        logger.error("CRITICAL ERROR:", Error)
