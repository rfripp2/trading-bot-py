from binance.error import ClientError
import logging
import pandas as pd
#import talib


def market_buy(quantity, bot):
    try:
        bot.clientFutures.new_order(
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


def limit_sell(price, quantity, bot):
    try:
        response = bot.clientFutures.new_order(
            symbol="BTCUSDT",
            side="SELL",
            type="LIMIT",
            timeInForce="GTC",
            price=price,
            quantity=quantity,
        )
        print("RESPONSE", response)
        logging.info(response)
        bot.order_pair["limit_sell_order_id"] = response["orderId"]

    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def stop_market(stopPrice, quantity, bot):
    try:
        response = bot.clientFutures.new_order(
            symbol="BTCUSDT",
            side="SELL",
            type="STOP_MARKET",
            quantity=quantity,
            timeInForce="GTC",
            stopPrice=stopPrice,
        )
        bot.order_pair["stop_sell_id"] = response["orderId"]
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
            symbol="BTCUSDT", limit=2, recvWindow=2000)
        return response
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_open_order(id, client):
    try:
        client.get_open_orders(symbol="BTCUSDT", orderId=id, recvWindow=2000)
    # logging.info(response)

    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_order(id, client):
    found = False
    all_orders = get_all_orders(client)
    for order in all_orders:
        if order["orderId"] == id:
            found = True
            return order
    if not found:
        print("not found")
        return False


def cancel_order(bot, id):
    try:
        response = bot.clientFutures.cancel_order(
            symbol="BTCUSDT", orderId=id, recvWindow=2000
        )
        logging.info(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def query_order(bot, id):
    try:
        response = bot.clientFutures.query_order(
            symbol="BTCUSDT", orderId=id, recvWindow=2000
        )
        logging.info(response)
        return response
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


"""def atr(client, timeframe):
    candles = client.klines("BTCUSDT", timeframe,
                            limit=15, contractType="perpetual")
    df = pd.DataFrame(candles)
    df["atr"] = talib.ATR(df[2], df[3], df[4], timeperiod=14)
    return float(df.iloc[-1]["atr"])
"""
