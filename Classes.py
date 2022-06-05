from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
from binance_orders import *
from logger import logger
from binance.error import ClientError, ServerError
from indicators import *


class Bot:
    def __init__(self, api_key, secret_key, timeframe, sma=2, ema=2):

        self.config = {"position_running": False}
        self.clientFutures = UMFutures(api_key, secret_key)
        self.timeframe = timeframe
        self.order_pair = {}
        self.closed_candels = []
        self.sma = sma
        self.my_client = UMFuturesWebsocketClient()
        self.balance = self.get_balance("USDT")
        self.ema = ema

    def get_balance(self, coin):
        assets = self.clientFutures.balance()
        for asset in assets:
            if asset['asset'] == coin:
                return float(asset['balance'])

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
                        and float(last_candle["c"]) > float(get_ema(self, self.ema))
                    ):
                        print("its bullish!")
                        ammount_to_buy = round(
                            self.balance / float(kline["c"]), 3)
                        market_buy(ammount_to_buy, self)
                        sell_stop_market_price = round(
                            float(kline["l"]) -
                            atr(self.clientFutures, self.timeframe), 2
                        )
                        stop_market(sell_stop_market_price,
                                    ammount_to_buy, self)

                        limit_sell_price = round(
                            (float(kline["c"]) -
                             sell_stop_market_price) * 1.25 + float(kline["c"]), 1)
                        limit_sell(limit_sell_price, ammount_to_buy, self)
                        self.config["position_running"] = True
                        self.stream_account_trades()
                    logger.info(kline)
                    logger.info(self.config['position_running'])
        except Exception as e:
            logger.error(e, "Error during bullisn engulfing handler")

    def run_bullish_engulfing(self):
        try:
            self.get_first_candels()
            self.my_client.start()
            self.my_client.continuous_kline(
                pair="btcusdt",
                id=1,
                contractType="perpetual",
                interval=self.timeframe,
                callback=self.bullish_engulfing_handler,
            )
        except ClientError as e:
            logger.error(e, "Error during bullisn engulfing run")

    def stream_account_trades(self):
        try:
            self.listen_key = self.clientFutures.new_listen_key()
            self.my_client.user_data(
                listen_key=self.listen_key["listenKey"],
                id=1,
                callback=self.account_message_handler,
            )

        except ClientError as e:
            logger.error(e, "Error during stream account trades")

    def account_message_handler(self, message):
        try:
            if message != None:
                order = message.get("o")
                if order and self.config['position_running'] and "i" in order and order['i'] == self.order_pair["stop_sell_id"]:
                    if order['X'] == "FILLED":
                        cancel_order(
                            self, self.order_pair["limit_sell_order_id"])
                        self.order_pair = {}
                        self.config['position_running'] = False

                elif order and self.config['position_running'] and "i" in order and order['i'] == self.order_pair["limit_sell_order_id"]:
                    if order['X'] == "FILLED":
                        cancel_order(self, self.order_pair["stop_sell_id"])
                        self.order_pair = {}
                        self.config['position_running'] = False

                if message.get("e") == 'listenKeyExpired':
                    logger.debug("renewing listen key!")
                    #self.listen_key = self.clientFutures.new_listen_key()
                    self.stream_account_trades()

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
