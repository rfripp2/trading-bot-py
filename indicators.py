import pandas as pd
import numpy as np
import talib


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


def get_ema(self, window):
    candles = self.clientFutures.klines(
        "BTCUSDT", self.timeframe, limit=150, contractType="perpetual"
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
    df[f"EMA_{window}"] = df['Close'].ewm(span=window, adjust=False).mean()
    last_ema = df.iloc[-1][f"EMA_{window}"]
    return float(last_ema)


def atr(client, timeframe):
    candles = client.klines("BTCUSDT", timeframe,
                            limit=50, contractType="perpetual")
    df = pd.DataFrame(candles)
    df["atr"] = talib.ATR(df[2], df[3], df[4], timeperiod=14)
    return float(df.iloc[-1]["atr"])
