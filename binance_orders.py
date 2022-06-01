from binance.error import ClientError
import pandas as pd
from logger import logger
#import talib


def market_buy(quantity, bot):
    try:
        response = bot.clientFutures.new_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=quantity,
        )

    except ClientError as error:
        logger.error(
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
        logger.info("response from limit sell", response)
        bot.order_pair["limit_sell_order_id"] = response["orderId"]

    except ClientError as error:
        logger.error(
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
        logger.info("response from stop market", response)
    except ClientError as error:
        logger.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_open_order(id, client):
    try:
        response = client.get_open_orders(
            symbol="BTCUSDT", orderId=id, recvWindow=2000)
        logger.error(response)

    except ClientError as error:
        logger.error(
            error
        )


def cancel_order(bot, id):
    try:
        response = bot.clientFutures.cancel_order(
            symbol="BTCUSDT", orderId=id, recvWindow=2000
        )
        logger.info(response)
    except ClientError as error:
        logger.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def query_order(bot, id):
    try:
        response = bot.clientFutures.query_order(
            symbol="BTCUSDT", orderId=id, recvWindow=2000
        )
        logger.info(response)
        return response
    except ClientError as error:
        logger.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def atr(client, timeframe):
    candles = client.klines("BTCUSDT", timeframe,
                            limit=15, contractType="perpetual")
    df = pd.DataFrame(candles)
    df["atr"] = talib.ATR(df[2], df[3], df[4], timeperiod=14)
    return float(df.iloc[-1]["atr"])
