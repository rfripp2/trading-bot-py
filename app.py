from fileinput import close
from sqlite3 import Timestamp
from tracemalloc import stop
from webbrowser import get
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

clientFutures = Futures(key=api_key, secret=secret_key)
position_running = False


def is_bulllishengulfing_listener(quantity):
    bullis_candle_stamps = []
    first_candle_open = clientFutures.klines(
        "BTCUSDT", "1m", limit=2, contractType="perpetual"
    )

    order_pairs = []
    closed_candels = [{"o": first_candle_open[0]
                       [1], "c": first_candle_open[0][4], "color": "unknwown"}]

    def message_handler(message):
        if (len(order_pairs) > 0):
            first_pair = order_pairs[0]
            if_filled_cancell_other(
                first_pair['limit_sell_order_id'], first_pair['stop_market_order_id'])
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
                    and position_running == False
                ):
                    print("its bullish!")
                    bullis_candle_stamps.append(kline["t"])
                    marketBuy(quantity)
                    limit_sell_price = get_limit_sell_price_from_price(
                        kline['c'], 1)
                    limitSell(quantity, limit_sell_price)
                    all_orders = get_all_orders()
                    limit_sell_order_id = all_orders[len(
                        all_orders)-1]['orderId']

                    sell_stop_market_price = get_stop_market_price_from_price(
                        kline['c'], 1)
                    stop_market(0.001, sell_stop_market_price)
                    all_orders = get_all_orders()
                    stop_market_order_id = all_orders[len(
                        all_orders)-1]['orderId']
                    order_pairs.append({"limit_sell_order_id": limit_sell_order_id,
                                        "stop_market_order_id": stop_market_order_id})
                    position_running = True
                print("order pairs", order_pairs)

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


def get_all_orders():
    try:
        response = clientFutures.get_all_orders(
            symbol="BTCUSDT", recvWindow=2000)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_open_order(id):
    try:
        response = clientFutures.get_open_orders(
            symbol="BTCUSDT", orderId=id, recvWindow=2000)
        logging.info(response)

    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_order(id):
    found = False
    all_orders = get_all_orders()
    for order in all_orders:
        if order['orderId'] == id:
            found = True
            return order
    if not found:
        print("not found")
        return False


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


def get_limit_sell_price_from_price(price, percentage):
    limit_sell_price = float(price) + (percentage * float(price) / 100)
    return int(limit_sell_price)


def get_stop_market_price_from_price(price, percentage):
    stop_sell_market_price = float(price) - (percentage * float(price) / 100)
    return int(stop_sell_market_price)


def if_filled_cancell_other(sell_limit_id, sell_stop_market_id):
    sell_limit_order = get_order(sell_limit_id)
    sell_stop_market_order = get_order(sell_stop_market_id)
    if sell_limit_order['status'] == 'FILLED':
        cancell_order(sell_stop_market_id)
    if sell_stop_market_order['status'] == "FILLED":
        cancell_order(sell_limit_id)


is_bulllishengulfing_listener(0.001)
## por ej marketBuy(0.001) el parametro es la cantidad a comprar ##
# marketBuy()
## por ej limitSell(0.001,30000) el parametro es la cantidad a comprar,y precio limit ##
# limitSell(0.001, 30200)
# para ver las ordenes y buscar un id si queres cancelarla
# get_all_orders()
# cancell_order(55200479125)
# stop_market(0.001,29800)
# get_limit_sell_price_from_price(80, 50)
# get_open_order(55200479125)
# get_order(None)
# get_stop_market_price_from_price(100, 10)
