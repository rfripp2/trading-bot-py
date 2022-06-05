from Classes import Bot
from dotenv import load_dotenv
import os
from logger import logger
from binance.error import ClientError, ServerError
load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")


bot = Bot(api_key=api_key, secret_key=secret_key, timeframe="1m", ema=50)


if __name__ == '__main__':
    try:
        bot.run_bullish_engulfing()
        logger.info("Bot running")

    except ClientError:
        bot.run_bullish_engulfing()
        logger.error("CRITICAL ERROR:", ClientError)
