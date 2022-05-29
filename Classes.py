from more_itertools import last
import pandas as pd
import numpy as np
from binance.websocket.futures.websocket_client import FuturesWebsocketClient as Client
from binance.futures import Futures
from dotenv import load_dotenv
import os
from binance.futures import Futures
from binance_orders import *

config_logging(logging, logging.DEBUG)


class Bot:
    def __init__(self, api_key, secret_key, balance, timeframe):
        self.balance = balance
        self.config = {"position_running": False}
        self.clientFutures = Futures(api_key, secret_key)
        self.timeframe = timeframe
        self.first_two_candels = self.clientFutures.klines(
            "BTCUSDT", "1m", limit=2, contractType="perpetual"
        )
        self.order_pair = {}
        self.closed_candels = [
            {
                "o": self.first_two_candels[0][1],
                "c": self.first_two_candels[0][4],
                "color": "unknwown",
            }
        ]

        self.counter = 0

    def bullish_engulfing_handler(self, message):

        kline = message.get("k")
        if kline != None:
            if kline["x"]:
                if bool(self.order_pair):
                    if_filled_cancell_other(
                        self.order_pair["limit_sell_order_id"],
                        self.order_pair["stop_market_order_id"],
                        self.clientFutures,
                        self,
                    )
                print("KLINE:", kline)
                if float(kline["c"]) > float(
                    self.closed_candels[len(self.closed_candels) - 1]["c"]
                ):
                    kline["color"] = "green"
                else:
                    kline["color"] = "red"
                self.closed_candels.append(kline)
                last_candle = self.closed_candels[-1]
                penultimate_candle = self.closed_candels[-2]

                if (
                    float(last_candle["c"]) > float(penultimate_candle["o"])
                    and penultimate_candle["color"] == "red"
                    and self.config["position_running"] == False
                ):
                    print("its bullish!")
                    ammount_to_buy = round(self.balance / float(kline["c"]), 3)
                    print("AMMOUNT TO BUY:", ammount_to_buy)
                    market_buy(ammount_to_buy, self.clientFutures)
                    sell_stop_market_price = round(
                        float(kline["l"]) - atr(self.clientFutures, self.timeframe), 2
                    )
                    stop_market(
                        sell_stop_market_price, ammount_to_buy, self.clientFutures
                    )

                    limit_sell_price = round(
                        float(kline["c"]) - sell_stop_market_price + float(kline["c"]),
                        1,
                    )

                    limit_sell(limit_sell_price, ammount_to_buy, self.clientFutures)
                    all_orders = get_all_orders(self.clientFutures)
                    limit_sell_order_id = all_orders[len(all_orders) - 2]["orderId"]
                    stop_market_order_id = all_orders[len(all_orders) - 1]["orderId"]
                    self.order_pair["limit_sell_order_id"] = limit_sell_order_id
                    self.order_pair["stop_market_order_id"] = stop_market_order_id
                    self.config["position_running"] = True

    def run_bullish_engulfing(self):
        my_client = Client()
        my_client.start()
        my_client.continuous_kline(
            pair="btcusdt",
            id=1,
            contractType="perpetual",
            interval=self.timeframe,
            callback=self.bullish_engulfing_handler,
        )

    def set_bankroll(self, bankroll):
        self.bankroll = bankroll

    def get_bankroll(self):
        print(self.bankroll)

    def get_sma(self, window):
        candles = self.clientFutures.klines(
            "BTCUSDT", self.timeframe, limit=window, contractType="perpetual"
        )
        pandas_array = np.array(candles)
        df = pd.DataFrame(
            pandas_array,
            columns=[
                "Open Time",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "Close time",
                "Quote asset volume",
                "Number of trades",
                "Taker buy base asset volume",
                "Taker buy quote asset volume",
                "Ignore",
            ],
        )
        df[f"SMA_{window}"] = df["Close"].rolling(window=int(window)).mean()
        last_sma = df.iloc[-1][f"SMA_{window}"]
        print(last_sma)
        return last_sma


# market_buy(0.002, bot.clientFutures)
# bot.run()
# market_buy(0.0029226093055880293, bot.clientFutures)
# stop_market(0.001, 28200.000, bot.clientFutures)
# limitSell(0.003, 29100.2, bot.clientFutures)
