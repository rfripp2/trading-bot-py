from binance.lib.utils import check_required_parameter
from binance.lib.utils import check_required_parameters


def ping(self):
    """
    |
    | **Test Connectivity**
    | *Test connectivity to the Rest API.*

    :API endpoint: ``GET /fapi/v1/ping``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#test-connectivity
    |
    """

    url_path = "/fapi/v1/ping"
    return self.query(url_path)


def time(self):
    """
    |
    | **Check Server Time**
    | *Test connectivity to the Rest API and get the current server time.*

    :API endpoint: ``GET /fapi/v1/time``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#check-server-time
    |
    """

    url_path = "/fapi/v1/time"
    return self.query(url_path)


def exchange_info(self):
    """
    |
    | **Exchange Information**
    | *Current exchange trading rules and symbol information.*

    :API endpoint: ``GET /fapi/v1/exchangeInfo``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#exchange-information
    |
    """

    url_path = "/fapi/v1/exchangeInfo"
    return self.query(url_path)


def depth(self, symbol: str, **kwargs):
    """
    |
    | **Order Book**

    :API endpoint: ``GET /fapi/v1/depth``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#order-book

    :parameter symbol: string.
    :parameter limit: optional int. Limit the results. Default 500, valid limits: [5, 10, 20, 50, 100, 500, 1000].
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/depth"
    return self.query(url_path, params)


def trades(self, symbol: str, **kwargs):
    """
    |
    | **Recent Trades List**
    | *Get recent market trades*

    :API endpoint: ``GET /fapi/v1/trades``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#recent-trades-list

    :parameter symbol: string.
    :parameter limit: optional int. Limit the results. Default 500, max 1000.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/trades"
    return self.query(url_path, params)


def historical_trades(self, symbol: str, **kwargs):
    """
    |
    | **Old Trade Lookup (MARKET_DATA)**
    | *Get older market historical trades.*

    :API endpoint: ``GET /fapi/v1/historicalTrades``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#old-trades-lookup-market_data

    :parameter symbol: string.
    :parameter limit: optional int. Limit the results. Default 500, max 1000.
    :parameter formId: optional int. Trade ID to fetch from. Default gets most recent trades.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/historicalTrades"
    return self.limit_request("GET", url_path, params)


def agg_trades(self, symbol: str, **kwargs):
    """
    |
    | **Compressed/Aggregate Trades List**
    | *Get compressed, aggregate market trades. Market trades that fill at the time, from the same order, with the same price will have the quantity aggregated.*
    
    :API endpoint: ``GET /fapi/v1/aggTrades``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list

    :parameter symbol: string.
    :parameter limit: optional int. Limit the results. Default 500, max 1000.
    :parameter formId: optional int. ID to get aggregate trades from INCLUSIVE.
    :parameter startTime: optional int. Timestamp in ms to get aggregate trades from INCLUSIVE.
    :parameter endTime: optional int. Timestamp in ms to get aggregate trades until INCLUSIVE.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/aggTrades"
    return self.query(url_path, params)


def klines(self, symbol: str, interval: str, **kwargs):
    """
    |
    | **Kline/Candlestick Data**
    | *Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.*

    :API endpoint: ``GET /fapi/v1/klines``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data

    :parameter symbol: string.
    :parameter interval: string. The interval of kline, e.g 1m, 5m, 1h, 1d, etc. (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 500, max 1500.
    :parameter startTime: optional int.
    :parameter endTime: optional int.
    |
    """

    check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
    params = {"symbol": symbol, "interval": interval, **kwargs}
    url_path = "/fapi/v1/klines"
    return self.query(url_path, params)


def continuous_klines(self, pair: str, contractType: str, interval: str, **kwargs):
    """
    |
    | **Continuous Kline/Candlestick Data**
    | *Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time.*  
    | *Klines are uniquely identified by their open time.*

    :API endpoint: ``GET /fapi/v1/continuousKlines``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#continuous-contract-kline-candlestick-data

    :parameter pair: string.
    :parameter contractType: string. PERPETUAL, CURRENT_MONTH, NEXT_MONTH, CURRENT_QUARTER, NEXT_QUARTER.
    :parameter interval: string. The interval of kline, e.g 1m, 5m, 1h, 1d, etc. (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 500, max 1500.
    :parameter startTime: optional int.
    :parameter endTime: optional int.
    |
    """

    check_required_parameters([[pair, "pair"], [contractType,"contractType"], [interval, "interval"]])
    params = {"pair": pair, "contractType":contractType, "interval": interval, **kwargs}
    url_path = "/fapi/v1/continuousKlines"
    return self.query(url_path, params)


def index_price_klines(self, pair: str, interval: str, **kwargs):
    """
    |
    | **Index Price Kline/Candlestick Data**
    | *Kline/Candlestick Data for the index price of a pair.*
    | *Klines are uniquely identified by their open time.*   
    
    :API endpoint: ``GET /fapi/v1/indexPriceKlines``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#index-price-kline-candlestick-data

    :parameter pair: string.
    :parameter interval: string. The interval of kline, e.g 1m, 5m, 1h, 1d, etc. (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 500, max 1500.
    :parameter startTime: optional int.
    :parameter endTime: optional int.
    |
    """

    check_required_parameters([[pair, "pair"], [interval, "interval"]])
    params = {"pair": pair, "interval": interval, **kwargs}
    url_path = "/fapi/v1/indexPriceKlines"
    return self.query(url_path, params)


def mark_price_klines(self, symbol: str, interval: str, **kwargs):
    """
    |
    | **Mark Price Kline/Candlestick Data**
    | *Kline/candlestick bars for the mark price of a symbol.*
    | *Klines are uniquely identified by their open time.*
    
    :API endpoint: ``GET /fapi/v1/markPriceKlines``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#mark-price-kline-candlestick-data

    :parameter symbol: string.
    :parameter interval: string. The interval of kline, e.g 1m, 5m, 1h, 1d, etc. (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 500, max 1500.
    :parameter startTime: optional int.
    :parameter endTime: optional int.
    |
    """

    check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
    params = {"symbol": symbol, "interval": interval, **kwargs}
    url_path = "/fapi/v1/markPriceKlines"
    return self.query(url_path, params)


def mark_price(self, symbol: str = None):
    """
    |
    | **Mark Price**
    | *Mark Price and Funding Rate*

    :API endpoint: ``GET /fapi/v1/premiumIndex``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#mark-price

    :parameter symbol: optional string.
    |
    """

    params = {"symbol": symbol}
    url_path = "/fapi/v1/premiumIndex"
    return self.query(url_path, params)


def funding_rate(self, symbol: str = None,  **kwargs):
    """
    |
    | **Get Funding Rate History**

    :API endpoint: ``GET /fapi/v1/fundingRate``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#get-funding-rate-history

    :parameter symbol: optional string.
    :parameter limit: optional int. Limit the results. Default 100, max 1000
    :parameter startTime: optional int. Timestamp in ms to get funding rate from INCLUSIVE.
    :parameter endTime: optional int. Timestamp in ms to get funding rate until INCLUSIVE.
    |
    """
    
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/fundingRate"
    return self.query(url_path, params)


def ticker_24hr_price_change(self, symbol: str = None):
    """
    |
    | **24hr Ticker Price Change Statistics**
    | *24 hour rolling window price change statistics.*
    | *Careful when accessing this with no symbol. If the symbol is not sent, tickers for all symbols will be returned in an array.*

    :API endpoint: ``GET /fapi/v1/ticker/24hr``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#24hr-ticker-price-change-statistics

    :parameter symbol: optional string.
    |
    """

    params = {"symbol": symbol}
    url_path = "/fapi/v1/ticker/24hr"
    return self.query(url_path, params)


def ticker_price(self, symbol: str = None):
    """
    |
    | **Symbol Price Ticker**
    | *Latest price for a symbol or symbols.*
    | *If the symbol is not sent, prices for all symbols will be returned in an array.*

    :API endpoint: ``GET /fapi/v1/ticker/price``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#symbol-price-ticker

    :parameter symbol: optional string.
    |
    """

    params = {"symbol": symbol}
    url_path = "/fapi/v1/ticker/price"
    return self.query(url_path, params)


def book_ticker(self, symbol: str = None):
    """
    |
    | **Symbol Order Book Ticker**
    | *Best price/qty on the order book for a symbol or symbols.*
    | *If the symbol is not sent, prices for all symbols will be returned in an array.*

    :API endpoint: ``GET /fapi/v1/ticker/bookTicker``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#symbol-order-book-ticker

    :parameter symbol: optional string; the trading symbol.
    |
    """

    params = {"symbol": symbol}
    url_path = "/fapi/v1/ticker/bookTicker"
    return self.query(url_path, params)


def open_interest(self, symbol: str):
    """
    |
    | **Open Interest**
    | *Get present open interest of a specific symbol.*

    :API endpoint: ``GET /fapi/v1/openInterest``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#open-interest

    :parameter symbol: string.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol}
    url_path = "/fapi/v1/openInterest"
    return self.query(url_path, params)


def open_interest_hist(self, symbol: str, period: str, **kwargs):
    """
    |
    | **Open Interest Statistics**
    | *Get historical open interest of a specific symbol.*
    
    :API endpoint: ``GET /futures/data/openInterestHist``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#open-interest-statistics

    :parameter symbol: string.
    :parameter period: string. The period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d".
    :parameter limit: optional int. Limit the results. Default 30, max 500.
    :parameter startTime: optional int. Only the data of the latest 30 days is available.
    :parameter endTime: optional int. Only the data of the latest 30 days is available.
    |
    """

    check_required_parameters([[symbol, "symbol"], [period, "period"]])
    params = {"symbol": symbol, "period": period, **kwargs}
    url_path = "/futures/data/openInterestHist"
    return self.query(url_path, params)


def top_long_short_account_ratio(self, symbol: str, period: str, **kwargs):
    """
    |
    | **Top Trader Long/Short Ratio (Accounts)**
    
    :API endpoint: ``GET /futures/data/topLongShortAccountRatio``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#top-trader-long-short-ratio-positions

    :parameter symbol: string.
    :parameter period: string. The period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 30, max 500.
    :parameter startTime: optional int. Only the data of the latest 30 days is available.
    :parameter endTime: optional int. Only the data of the latest 30 days is available.
    |
    """

    check_required_parameters([[symbol, "symbol"], [period, "period"]])
    params = {"symbol": symbol, "period": period, **kwargs}
    url_path = "/futures/data/topLongShortAccountRatio"
    return self.query(url_path, params)


def top_long_short_position_ratio(self, symbol: str, period: str, **kwargs):
    """
    |
    | **Top Trader Long/Short Ratio (Positions)**
    
    :API endpoint: ``GET /futures/data/topLongShortPositionRatio``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#top-trader-long-short-ratio-positions

    :parameter symbol: string.
    :parameter period: string. The period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 30, max 500.
    :parameter startTime: optional int. Only the data of the latest 30 days is available.
    :parameter endTime: optional int. Only the data of the latest 30 days is available.
    |
    """

    check_required_parameters([[symbol, "symbol"], [period, "period"]])
    params = {"symbol": symbol, "period": period, **kwargs}
    url_path = "/futures/data/topLongShortPositionRatio"
    return self.query(url_path, params)


def long_short_account_ratio(self, symbol: str, period: str, **kwargs):
    """
    |
    | **Long/Short Ratio**
    
    :API endpoint: ``GET /futures/data/globalLongShortAccountRatio``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#long-short-ratio

    :parameter symbol: string.
    :parameter period: string. The period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 30, max 500.
    :parameter startTime: optional int. Only the data of the latest 30 days is available.
    :parameter endTime: optional int. Only the data of the latest 30 days is available.
    |
    """

    check_required_parameters([[symbol, "symbol"], [period, "period"]])
    params = {"symbol": symbol, "period": period, **kwargs}
    url_path = "/futures/data/globalLongShortAccountRatio"
    return self.query(url_path, params)


def taker_long_short_ratio(self, symbol: str, period: str, **kwargs):
    """
    |
    | **Taker Buy/Sell Volume**
    
    :API endpoint: ``GET /futures/data/takerlongshortRatio``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#taker-buy-sell-volume

    :parameter symbol: string.
    :parameter period: string. The period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 30, max 500.
    :parameter startTime: optional int. Only the data of the latest 30 days is available.
    :parameter endTime: optional int. Only the data of the latest 30 days is available.
    |
    """

    check_required_parameters([[symbol, "symbol"], [period, "period"]])
    params = {"symbol": symbol, "period": period, **kwargs}
    url_path = "/futures/data/takerlongshortRatio"
    return self.query(url_path, params)


def blvt_kline(self, symbol: str, interval: str, **kwargs):
    """
    |
    | **Historical BLVT NAV Kline/Candlestick**
    | *The BLVT NAV system is based on Binance Futures, so the endpoint is based on fapi*
    
    :API endpoint: ``GET /fapi/v1/lvtKlines``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#historical-blvt-nav-kline-candlestick

    :parameter symbol: string. The token name, e.g. "BTCDOWN", "BTCUP".
    :parameter period: string. The period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info)
    :parameter limit: optional int. Limit the results. Default 500, max 1000.
    :parameter startTime: optional int.
    :parameter endTime: optional int.
    |
    """

    check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
    params = {"symbol": symbol, "interval": interval, **kwargs}
    url_path = "/fapi/v1/lvtKlines"
    return self.query(url_path, params)


def index_info(self, symbol: str = None):
    """
    |
    | **Composite Index Symbol Information**

    :API endpoint: ``GET /fapi/v1/indexInfo``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#composite-index-symbol-information

    :parameter symbol: optional string. The trading symbol. Only for composite index symbols.
    |
    """

    params = {"symbol": symbol}
    url_path = "/fapi/v1/indexInfo"
    return self.query(url_path, params)


def asset_index(self, symbol: str = None):
    """
    |
    | **Multi-Assets Mode Asset Index**
    | *Asset index for Multi-Assets mode*

    :API endpoint: ``GET /fapi/v1/assetIndex``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#multi-assets-mode-asset-index

    :parameter symbol: optional string. Asset pair in multi asset mode (ex: BTCUSD).
    |
    """

    params = {"symbol": symbol}
    url_path = "/fapi/v1/assetIndex"
    return self.query(url_path, params)
