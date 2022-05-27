import pandas as pd
import numpy as np
import time
from urllib.parse import urlencode, urljoin
from binance.websocket.futures.websocket_client import FuturesWebsocketClient as Client
from binance.futures import Futures
from dotenv import load_dotenv
import os
from binance.futures import Futures
from binance.error import ClientError
from binance.lib.utils import config_logging
import logging
from binance_orders import *
load_dotenv()


class Bot():
    def __init__(self, quantity):
        self.quantity = quantity
        self.config = {
            "position_running": False
        }
        self.clientFutures = Futures(key=os.getenv("API_KEY"),
                                     secret=os.getenv("SECRET_KEY"))

    def bullish_engulfing_handler(self, message):
        first_two_candels = self.clientFutures.klines(
            "BTCUSDT", "1m", limit=2, contractType="perpetual"
        )
        order_pairs = []
        closed_candels = [{"o": first_two_candels[0]
                           [1], "c": first_two_candels[0][4], "color": "unknwown"}]
        if (len(order_pairs) > 0):
            first_pair = order_pairs[0]
            if_filled_cancell_other(
                first_pair['limit_sell_order_id'], first_pair['stop_market_order_id'])
        kline = message.get("k")
        if kline != None:
            if kline["x"]:
                print("KLINE:", kline)
                if kline["c"] > closed_candels[len(closed_candels) - 1]["c"]:
                    kline["color"] = "green"
                else:
                    kline["color"] = "red"
                closed_candels.append(kline)
                last_candle = closed_candels[-1]
                penultimate_candle = closed_candels[-2]
                if (
                    last_candle["c"]
                    > penultimate_candle["o"]
                    and penultimate_candle["color"] == "red"
                    and self.config['position_running'] == False
                ):
                    print("its bullish!")
                    market_buy(self.quantity, self.clientFutures)
                    limit_sell_price = get_limit_sell_price_from_price(
                        kline['c'], 1)
                    limitSell(self.quantity, limit_sell_price,
                              self.clientFutures)
                    all_orders = get_all_orders()
                    limit_sell_order_id = all_orders[len(
                        all_orders)-1]['orderId']

                    sell_stop_market_price = get_stop_market_price_from_price(
                        kline['c'], 1)
                    stop_market(0.001, sell_stop_market_price,
                                self.clientFutures)
                    all_orders = get_all_orders()
                    stop_market_order_id = all_orders[len(
                        all_orders)-1]['orderId']
                    order_pairs.append({"limit_sell_order_id": limit_sell_order_id,
                                        "stop_market_order_id": stop_market_order_id})
                    self.config['position_running'] = True
                print("order pairs", order_pairs)

    def run(self):
        my_client = Client()
        my_client.start()
        my_client.continuous_kline(
            pair="btcusdt",
            id=1,
            contractType="perpetual",
            interval="1m",
            callback=self.bullish_engulfing_handler,
        )

    def set_bankroll(self, bankroll):
        self.bankroll = bankroll

    def get_bankroll(self):
        print(self.bankroll)

    def get_sma(self, window):
        candles = self.clientFutures.klines(
            "BTCUSDT", "1m", limit=50, contractType="perpetual"
        )
        pandas_array = np.array(candles)
        df = pd.DataFrame(pandas_array, columns=['Open Time',
                                                 'Open',
                                                 'High',
                                                 'Low',
                                                 'Close',
                                                 'Volume',
                                                 'Close time',
                                                 'Quote asset volume',
                                                 'Number of trades',
                                                 'Taker buy base asset volume',
                                                 'Taker buy quote asset volume',
                                                 'Ignore'])
        df[f"SMA_{window}"] = df['Close'].rolling(window=int(window)).mean()
        last_sma = df.iloc[-1][f"SMA_{window}"]
        print(str(last_sma))
        return str(last_sma)


bot = Bot(0.001)
bot.run()
