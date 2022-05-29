from Classes import Bot
import numpy as np
import pandas as pd
import talib
from tracemalloc import stop
from webbrowser import get
from dotenv import load_dotenv
import os
from binance_orders import *

load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")


bot = Bot(api_key=api_key, secret_key=secret_key, balance=80, timeframe="1m")
bot.run_bullish_engulfing()
get_all_orders(bot.clientFutures)
