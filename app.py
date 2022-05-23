from fileinput import close
from sqlite3 import Timestamp
from typing_extensions import Self
from dotenv import load_dotenv
import os
import json
import time
import logging
from urllib.parse import urlencode, urljoin
import hmac
import hashlib
import requests
from binance.futures import Futures
from binance.error import ClientError
from binance.websocket.futures.websocket_client import FuturesWebsocketClient as Client
from binance.lib.utils import config_logging


config_logging(logging, logging.DEBUG)
load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")
headers = {
    'X-MBX-APIKEY': api_key
}

print(api_key)
clientFutures = Futures(key=api_key, secret=secret_key)


def isBulllishEngulfing():
    bullis_candle_stamps = []
    first_candle_open = clientFutures.klines(
        "BTCUSDT", "1m", limit=2, contractType="perpetual"
    )

    closed_candels = [{"o": first_candle_open[0]
                       [1], "c": first_candle_open[0][4], "color": "unknwown"}]

    def message_handler(message):
        kline = message.get("k")
        if kline != None:
            if kline["x"]:
                if kline["c"] > closed_candels[len(closed_candels) - 1]["c"]:
                    kline["color"] = "green"
                else:
                    kline["color"] = "red"
                closed_candels.append(kline)
                if (
                    closed_candels[len(closed_candels) - 1]["c"]
                    > closed_candels[len(closed_candels) - 2]["o"]
                    and closed_candels[len(closed_candels) - 2]["color"] == "red"
                ):
                    print("its bullish!")
                    print(closed_candels[len(closed_candels) - 2]['o'],
                          closed_candels[len(closed_candels)-1]['c'])
                    bullis_candle_stamps.append(kline["t"])
                print(bullis_candle_stamps)

    my_client = Client()
    my_client.start()
    my_client.continuous_kline(
        pair="btcusdt",
        id=1,
        contractType="perpetual",
        interval="1m",
        callback=message_handler,
    )
    """time.sleep(2)

    logging.debug("closing ws connection")"""


def marketBuy(quantity):
    try:
        response = clientFutures.new_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=quantity,
        )

    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def limitSell(quantity, price):
    try:
        response = clientFutures.new_order(
            symbol="BTCUSDT",
            side="SELL",
            type="LIMIT",
            quantity=quantity,
            timeInForce="GTC",
            price=price,
        )
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def stop_market(quantity, stopPrice):
    try:
        response = clientFutures.new_order(
            symbol="BTCUSDT",
            side="SELL",
            type="STOP_MARKET",
            quantity=quantity,
            timeInForce="GTC",
            stopPrice=stopPrice
        )
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_open_orders():
    try:
        response = clientFutures.get_orders(symbol="BTCUSDT", recvWindow=2000)
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def cancell_order(id):
    PATH = '/fapi/v1/order'
    BASE_URL = 'https://fapi.binance.com'
    timestamp = int(time.time() * 1000)
    try:
        params = {
            "symbol": "BTCUSDT",
            "orderId": id,
            'timestamp': timestamp
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(secret_key.encode(
            'utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, PATH)
        r = requests.delete(url, headers=headers, params=params)
        logging.info(r.json())
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )

        )


# isBulllishEngulfing()
## por ej marketBuy(0.001) el parametro es la cantidad a comprar ##
# marketBuy()
## por ej limitSell(0.001,30000) el parametro es la cantidad a comprar,y precio limit ##
#limitSell(0.001, 30200)
# para ver las ordenes y buscar un id si queres cancelarla
# get_open_orders()
# cancell_order(id)
# stop_market(0.001,29800)
