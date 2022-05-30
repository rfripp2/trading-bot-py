import pandas as pd
import numpy as np
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
from binance_orders import *


class Bot:
    def __init__(self, api_key, secret_key, balance, timeframe, sma):
        self.balance = balance
        self.config = {"position_running": False}
        self.clientFutures = UMFutures(api_key, secret_key)
        self.timeframe = timeframe
        self.order_pair = {}
        self.closed_candels = []
        self.sma = sma

    def bullish_engulfing_handler(self, message):

        kline = message.get("k")
        if kline != None:
            if kline["x"]:
                if bool(self.order_pair):
                    self.if_filled_cancel_other(
                        self.order_pair["limit_sell_order_id"],
                        self.order_pair["stop_sell_id"],
                    )
                print("KLINE:", kline)
                if float(kline["c"]) > float(self.closed_candels[-1]["c"]):
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
                    and float(last_candle["c"]) > float(self.get_sma(self.sma))
                ):
                    print("its bullish!")
                    ammount_to_buy = round(self.balance / float(kline["c"]), 3)
                    market_buy(ammount_to_buy, self)
                    sell_stop_market_price = round(
                        float(kline["l"]) - atr(self.clientFutures, self.timeframe), 2
                    )
                    stop_market(sell_stop_market_price, ammount_to_buy, self)

                    limit_sell_price = round(
                        float(kline["c"]) - sell_stop_market_price + float(kline["c"]),
                        1,
                    )

                    limit_sell(limit_sell_price, ammount_to_buy, self)
                    self.config["position_running"] = True

    def run_bullish_engulfing(self):
        my_client = UMFuturesWebsocketClient()
        self.get_first_candels()
        my_client.start()
        my_client.continuous_kline(
            pair="btcusdt",
            id=1,
            contractType="perpetual",
            interval=self.timeframe,
            callback=self.bullish_engulfing_handler,
        )

    def get_first_candels(self):
        first_candels = self.clientFutures.klines(
            "BTCUSDT", self.timeframe, limit=3, contractType="perpetual"
        )

        if float(first_candels[-2][4]) > float(first_candels[-3][4]):
            self.closed_candels.append(
                {
                    "o": first_candels[-2][1],
                    "c": first_candels[-2][4],
                    "color": "green",
                }
            )
        else:
            self.closed_candels.append(
                {
                    "o": first_candels[-2][1],
                    "c": first_candels[-2][4],
                    "color": "red",
                }
            )

        print(self.closed_candels)

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
        return float(last_sma)

    def if_filled_cancel_other(self, limit_sell_id, stop_sell_id):
        sell_limit_order = query_order(self, limit_sell_id)
        sell_stop_market_order = query_order(self, stop_sell_id)
        if sell_limit_order["status"] == "FILLED":
            cancel_order(self, stop_sell_id)
            self.config["position_running"] = False
            self.order_pair = {}

        if sell_stop_market_order["status"] == "FILLED":
            cancel_order(self, limit_sell_id)
            self.config["position_running"] = False
            self.order_pair = {}


# market_buy(0.002, bot.clientFutures)
# bot.run()
# market_buy(0.0029226093055880293, bot.clientFutures)
# stop_market(0.001, 28200.000, bot.clientFutures)
# limitSell(0.003, 29100.2, bot.clientFutures)
