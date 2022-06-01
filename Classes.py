from msilib.schema import Error
from xmlrpc.client import Server
import pandas as pd
import numpy as np
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
from binance_orders import *
from logger import logger
from binance.error import ClientError, ServerError


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
        try:
            kline = message.get("k")
            if kline != None:
                if kline["x"]:
                    if float(kline["c"]) > float(self.closed_candels[-1]["c"]):
                        kline["color"] = "green"
                    else:
                        kline["color"] = "red"
                    self.closed_candels.append(kline)
                    last_candle = self.closed_candels[-1]
                    penultimate_candle = self.closed_candels[-2]

                    if (
                        float(last_candle["c"]) > float(
                            penultimate_candle["o"])
                        and penultimate_candle["color"] == "red"
                        and self.config["position_running"] == False
                        # and float(last_candle["c"]) > float(self.get_sma(self.sma))
                    ):
                        print("its bullish!")
                        ammount_to_buy = round(
                            self.balance / float(kline["c"]), 3)
                        market_buy(ammount_to_buy, self)
                        sell_stop_market_price = round(
                            float(kline["l"]) -
                            35, 2
                        )
                        stop_market(sell_stop_market_price,
                                    ammount_to_buy, self)

                        limit_sell_price = round(
                            float(kline["c"]) -
                            sell_stop_market_price + float(kline["c"]),
                            1,
                        )
                        limit_sell(limit_sell_price, ammount_to_buy, self)
                        self.config["position_running"] = True
                    logger.info(kline)
                    logger.info(self.config['position_running'])
        except Exception as e:
            logger.error(e, "Error during bullisn engulfing handler")

    def run_bullish_engulfing(self):
        try:
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
        except Error as e:
            logger.error(e, "Error during bullisn engulfing run")

    def stream_account_trades(self):
        try:
            client = self.clientFutures
            response = client.new_listen_key()
            ws_client = UMFuturesWebsocketClient()
            ws_client.start()
            ws_client.user_data(
                listen_key=response["listenKey"],
                id=1,
                callback=self.account_message_handler,
            )
        except Error as e:
            logger.error(e, "Error during stream account trades")

    def account_message_handler(self, message):
        try:
            if message != None:
                message = message.get("o")
                logger.debug(
                    f"Message:{message}")
                if message and self.config['position_running'] and "i" in message and message['i'] == self.order_pair["stop_sell_id"]:
                    if message['X'] == "FILLED":
                        cancel_order(
                            self, self.order_pair["limit_sell_order_id"])
                        self.order_pair = {}
                        self.config['position_running'] = False
                elif message and self.config['position_running'] and "i" in message and message['i'] == self.order_pair["limit_sell_order_id"]:
                    if message['X'] == "FILLED":
                        cancel_order(self, self.order_pair["stop_sell_id"])
                        self.order_pair = {}
                        self.config['position_running'] = False

        except ClientError:
            logger.error(ClientError, "Error during stream account trades")

        except ServerError:
            logger.error(ServerError, "error during stream trades,server side")

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
        return float(last_sma)
