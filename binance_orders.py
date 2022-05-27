from concurrent.futures import process
import time
from binance.websocket.futures.websocket_client import FuturesWebsocketClient as Client
from binance.futures import Futures
from dotenv import load_dotenv
import os
from binance.futures import Futures
from binance.error import ClientError
from binance.lib.utils import config_logging
import logging
from urllib.parse import urlencode, urljoin
import requests
import hmac
import hashlib
import pandas as pd
import numpy as np


def market_buy(quantity, client):
    try:
        client.new_order(
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


def limitSell(quantity, price, client):
    try:
        response = client.new_order(
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


def stop_market(quantity, stopPrice, client):
    try:
        response = client.new_order(
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


def get_all_orders(client):
    try:
        response = client.get_all_orders(
            symbol="BTCUSDT", recvWindow=2000)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_open_order(id, client):
    try:
        client.get_open_orders(
            symbol="BTCUSDT", orderId=id, recvWindow=2000)
    # logging.info(response)

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
    secret_key = os.getenv("SECRET_KEY")
    api_key = os.getenv("API_KEY")
    headers = {
        'X-MBX-APIKEY': api_key
    }
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


def get_sma(window, client):
    candles = client.klines(
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
