from binance.lib.utils import check_required_parameter
from binance.lib.utils import check_required_parameters


def ping(self):
    """
    |
    | **Test Connectivity**
    | *Test connectivity to the Rest API.*

    :API endpoint: ``GET /dapi/v1/ping``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#test-connectivity
    |
    """

    url_path = "/dapi/v1/ping"
    return self.query(url_path)


def time(self):
    """
    |
    | **Check Server Time**
    | *Test connectivity to the Rest API and get the current server time.*

    :API endpoint: ``GET /dapi/v1/time``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#check-server-time
    |
    """

    url_path = "/dapi/v1/time"
    return self.query(url_path)


def exchange_info(self):
    """
    |
    | **Exchange Information**
    | *Current exchange trading rules and symbol information*

    :API endpoint: ``GET /dapi/v1/exchangeInfo``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#exchange-information
    |
    """

    url_path = "/dapi/v1/exchangeInfo"
    return self.query(url_path)


def depth(self, symbol: str, **kwargs):
    """
    |
    | **Order Book**

    :API endpoint: ``GET /dapi/v1/depth``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#order-book

    :parameter symbol: string; the trading pair.
    :parameter limit: optional int; limit the results. Default 500, valid limits: [5, 10, 20, 50, 100, 500, 1000].
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    return self.query("/dapi/v1/depth", params)


def trades(self, symbol: str, **kwargs):
    """
    |
    | **Recent Trades List**
    | *Get recent market trades.*

    :API endpoint: ``GET /dapi/v1/trades``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#recent-trades-list

    :parameter symbol: string; the trading pair.
    :parameter limit: optional int; limit the results. Default 500, max 1000.
    |
    """
    
    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    return self.query("/dapi/v1/trades", params)


def historical_trades(self, symbol: str, **kwargs):
    """
    |
    | **Old Trades Lookup (MARKET_DATA)**
    | *Get older market historical trades.*

    :API endpoint: ``GET /dapi/v1/historicalTrades``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#old-trades-lookup-market_data

    :parameter symbol: string; the trading pair.
    :parameter limit: optional int; limit the results. Default 500, max 1000.
    :parameter formId: optional long. TradeId to fetch from. Default gets most recent trades.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    return self.limit_request("GET", "/dapi/v1/historicalTrades", params)


def agg_trades(self, symbol: str, **kwargs):
    """
    |
    | **Compressed/Aggregate Trades List**
    | *Get compressed, aggregate market trades. Market trades that fill at the time, from the same order, with the same price will have the quantity aggregated.*
    
    :API endpoint: ``GET /dapi/v1/aggTrades``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#compressed-aggregate-trades-list

    :parameter symbol: string; the trading pair.
    :parameter limit: optional int; limit the results. Default 500, max 1000.
    :parameter formId: optional long. Trade ID to fetch from. Default gets most recent trades.
    :parameter startTime: optional long. Timestamp in ms to get aggregate trades from INCLUSIVE.
    :parameter endTime: optional long. Timestamp in ms to get aggregate trades until INCLUSIVE.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    return self.query("/dapi/v1/aggTrades", params)


def klines(self, symbol: str, interval: str, **kwargs):
    """
    |
    | **Kline/Candlestick Data**
    | *Kline/candlestick bars for a symbol.*
    | *Klines are uniquely identified by their open time.*

    :API endpoint: ``GET /dapi/v1/klines``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#kline-candlestick-data

    :parameter symbol: string; the trading pair.
    :parameter interval: string; the interval of kline, e.g 1m, 5m, 1h, 1d, etc. (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 500, max 1500.
    :parameter startTime: optional long. Timestamp in ms to get aggregate trades from INCLUSIVE.
    :parameter endTime: optional long. Timestamp in ms to get aggregate trades until INCLUSIVE.
    |
    """

    check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
    params = {"symbol": symbol, "interval": interval, **kwargs}
    return self.query("/dapi/v1/klines", params)


def continuous_klines(self, pair: str, contractType: str, interval: str, **kwargs):
    """
    |
    | **Continuous Contract Kline/Candlestick Data**
    | *Kline/candlestick bars for a specific contract type.*
    | *Klines are uniquely identified by their open time.*  
    
    :API endpoint: ``GET /dapi/v1/continuousKlines``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#continuous-contract-kline-candlestick-data

    :parameter pair: string; the trading pair.
    :parameter contractType: string; PERPETUAL, CURRENT_QUARTER, NEXT_QUARTER.
    :parameter interval: string; the interval of kline, e.g 1m, 5m, 1h, 1d, etc. (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 500, max 1500.
    :parameter startTime: optional long. Timestamp in ms to get aggregate trades from INCLUSIVE.
    :parameter endTime: optional long. Timestamp in ms to get aggregate trades until INCLUSIVE.
    |
    """

    check_required_parameters([[pair, "pair"], [contractType,"contractType"], [interval, "interval"]])
    params = {"pair": pair, "contractType":contractType, "interval": interval, **kwargs}
    return self.query("/dapi/v1/continuousKlines", params)


def index_price_klines(self, pair: str, interval: str, **kwargs):
    """
    |
    | **Index Price Kline/Candlestick Data**
    | *Kline/candlestick bars for the index price of a pair.*
    | *Klines are uniquely identified by their open time.*  
    
    :API endpoint: ``GET /dapi/v1/indexPriceKlines``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#index-price-kline-candlestick-data

    :parameter pair: string; the trading pair.
    :parameter interval: string; the interval of kline, e.g 1m, 5m, 1h, 1d, etc. (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 500, max 1500.
    :parameter startTime: optional long. Timestamp in ms to get aggregate trades from INCLUSIVE.
    :parameter endTime: optional long. Timestamp in ms to get aggregate trades until INCLUSIVE.
    |
    """

    check_required_parameters([[pair, "pair"], [interval, "interval"]])
    params = {"pair": pair, "interval": interval, **kwargs}
    return self.query("/dapi/v1/indexPriceKlines", params)


def mark_price_klines(self, symbol: str, interval: str, **kwargs):
    """
    |
    | **Mark Price Kline/Candlestick Data*
    | *Kline/candlestick bars for the mark price of a symbol.*
    | *Klines are uniquely identified by their open time.*
    
    :API endpoint: ``GET /dapi/v1/markPriceKlines``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#mark-price-kline-candlestick-data

    :parameter pair: string; the trading pair.
    :parameter interval: string; the interval of kline, e.g 1m, 5m, 1h, 1d, etc. (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 500, max 1500.
    :parameter startTime: optional long. Timestamp in ms to get aggregate trades from INCLUSIVE.
    :parameter endTime: optional long. Timestamp in ms to get aggregate trades until INCLUSIVE.
    |
    """

    check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
    params = {"symbol": symbol, "interval": interval, **kwargs}
    return self.query("/dapi/v1/markPriceKlines", params)


def ticker_24hr_price_change(self, symbol: str = None, pair: str = None):
    """
    |
    | **24hr Ticker Price Change Statistics**
    | *24 hour rolling window price change statistics.*
    | *Careful when accessing this with no symbol.*
    | *Symbol and pair cannot be sent together. If a pair is sent,tickers for all symbols of the pair will be returned. If either a pair or symbol is sent, tickers for all symbols of all pairs will be returned.*

    :API endpoint: ``GET /dapi/v1/ticker/24hr``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#24hr-ticker-price-change-statistics

    :parameter symbol: optional string; the trading symbol.
    :parameter pair: optional string; the trading pair.
    |
    """

    if (symbol is None) and (pair is None):
        return self.query("/dapi/v1/ticker/24hr")
    elif (symbol is None):
        params = {"pair": pair}
    else:
        params = {"symbol": symbol}

    return self.query("/dapi/v1/ticker/24hr", params)


def mark_price(self, symbol: str = None, pair: str = None):
    """
    |
    | **Index Price and Mark Price**

    :API endpoint: ``GET /dapi/v1/premiumIndex``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#index-price-and-mark-price

    :parameter symbol: optional string; the trading symbol.
    :parameter pair: optional string; the trading pair.
    |
    """

    if (symbol is None) and (pair is None):
        return self.query("/dapi/v1/premiumIndex")
    elif (symbol is None):
        params = {"pair": pair}
    else:
        params = {"symbol": symbol}

    return self.query("/dapi/v1/premiumIndex", params)


def funding_rate(self, symbol: str, **kwargs):
    """
    |
    | **Get Funding Rate History of Perpetual Futures**

    :API endpoint: ``GET /dapi/v1/fundingRate``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#get-funding-rate-history-of-perpetual-futures

    :parameter symbol: string; the trading pair. Empty array will be returned for delivery symbols.
    :parameter limit: optional int; limit the results. Default 100, max 1000.
    :parameter startTime: optional long. Timestamp in ms to get aggregate trades from INCLUSIVE.
    :parameter endTime: optional long. Timestamp in ms to get aggregate trades until INCLUSIVE.
    |
    """
    
    params = {"symbol": symbol, **kwargs}
    return self.query("/dapi/v1/fundingRate", params)


def ticker_price(self, symbol: str = None, pair: str = None):
    """
    |
    | **Symbol Price Ticker**

    :API endpoint: ``GET /dapi/v1/ticker/price``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#symbol-price-ticker

    :parameter symbol: optional string; the trading symbol.
    :parameter pair: optional string; the trading pair.
    |
    """

    if (symbol is None) and (pair is None):
        return self.query("/dapi/v1/ticker/price")
    elif (symbol is None):
        params = {"pair": pair}
    else:
        params = {"symbol": symbol}

    return self.query("/dapi/v1/ticker/price", params)


def book_ticker(self, symbol: str = None, pair: str = None):
    """
    |
    | **Symbol Order Book Ticker**
    | *Best price/qty on the order book for a symbol or symbols.*

    :API endpoint: ``GET /dapi/v1/ticker/bookTicker``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#symbol-order-book-ticker

    :parameter symbol: optional string; the trading symbol.
    :parameter pair: optional string; the trading pair.
    |
    """

    if (symbol is None) and (pair is None):
        return self.query("/dapi/v1/ticker/bookTicker")
    elif (symbol is None):
        params = {"pair": pair}
    else:
        params = {"symbol": symbol}

    return self.query("/dapi/v1/ticker/bookTicker", params)


def open_interest(self, symbol: str):
    """
    |
    | **Open Interest**
    | *Get present open interest of a specific symbol.*

    :API endpoint: ``GET /dapi/v1/openInterest``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#open-interest

    :parameter symbol: string; the trading symbol.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol}
    return self.query("/dapi/v1/openInterest", params)


def open_interest_hist(self, pair: str, contractType: str, period: str, **kwargs):
    """
    |
    | **Open Interest Statistics**
    
    :API endpoint: ``GET /futures/data/openInterestHist``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#open-interest-statistics-market-data

    :parameter pair: string; the trading pair.
    :parameter contractType: string; ALL, CURRENT_QUARTER, NEXT_QUARTER, PERPETUAL.
    :parameter period: string; the period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 30, max 500.
    :parameter startTime: optional long.
    :parameter endTime: optional long.
    |
    """

    check_required_parameters([[pair, "pair"], [contractType, "contractType"], [period, "period"]])
    params = {"pair": pair, "contractType": contractType, "period": period, **kwargs}
    return self.query("/futures/data/openInterestHist", params)


def top_long_short_account_ratio(self, pair: str, period: str, **kwargs):
    """
    |
    | **Top Trader Long/Short Ratio (Accounts)**
    
    :API endpoint: `GET /futures/data/topLongShortAccountRatio`
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#top-trader-long-short-ratio-accounts-market-data

    :parameter pair: string; the trading pair.
    :parameter period: string; the period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 30, max 500.
    :parameter startTime: optional long.
    :parameter endTime: optional long.
    |
    """

    check_required_parameters([[pair, "pair"], [period, "period"]])
    params = {"pair": pair, "period": period, **kwargs}
    return self.query("/futures/data/topLongShortAccountRatio", params)


def top_long_short_position_ratio(self, pair: str, period: str, **kwargs):
    """
    |
    | **Top Trader Long/Short Ratio (Positions)**
    
    :API endpoint: ``GET /futures/data/topLongShortPositionRatio``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#top-trader-long-short-ratio-positions-market-data

    :parameter pair: string; the trading pair
    :parameter period: string; the period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 30, max 500.
    :parameter startTime: optional long.
    :parameter endTime: optional long.
    |
    """

    check_required_parameters([[pair, "pair"], [period, "period"]])
    params = {"pair": pair, "period": period, **kwargs}
    return self.query("/futures/data/topLongShortPositionRatio", params)


def long_short_account_ratio(self, pair: str, period: str, **kwargs):
    """
    |
    | **Long/Short Ratio**
    
    :API endpoint: ``GET /futures/data/globalLongShortAccountRatio``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#top-trader-long-short-ratio-accounts-market-data

    :parameter pair: string; the trading pair
    :parameter period: string; the period of open interest, "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 30, max 500.
    :parameter startTime: optional long.
    :parameter endTime: optional long.
    |
    """

    check_required_parameters([[pair, "pair"], [period, "period"]])
    params = {"pair": pair, "period": period, **kwargs}
    return self.query("/futures/data/globalLongShortAccountRatio", params)


def taker_long_short_ratio(self, pair: str, contractType: str, period: str, **kwargs):
    """
    |
    | **Taker Buy/Sell Volume**
    
    :API endpoint: ``GET /futures/data/takerBuySellVol``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#taker-buy-sell-volume-market-data

    :parameter pair: string; the trading pair.
    :parameter contractType: string. ALL, CURRENT_QUARTER, NEXT_QUARTER, PERPETUAL.
    :parameter period: string. "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 30, max 500.
    :parameter startTime: optional long.
    :parameter endTime: optional long.
    |
    """

    check_required_parameters([[pair, "pair"], [contractType, "contractType"], [period, "period"]])
    params = {"pair": pair, "contractType": contractType, "period": period, **kwargs}
    return self.query("/futures/data/takerBuySellVol", params)


def basis(self, pair: str, contractType: str, period: str, **kwargs):
    """
    |
    | **Basis**

    :API endpoint: ``GET /futures/data/basis``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#basis-market-data

    :parameter pair: string; the trading pair.
    :parameter contractType: string; CURRENT_QUARTER, NEXT_QUARTER, PERPETUAL.
    :parameter period: string. "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d". (see more in https://binance-docs.github.io/apidocs/delivery/en/#public-endpoints-info)
    :parameter limit: optional int; limit the results. Default 30, max 500.
    :parameter startTime: optional long.
    :parameter endTime: optional long.
    |
    """

    check_required_parameters([[pair, "pair"], [contractType, "contractType"], [period, "period"]])
    params = {"pair": pair, "contractType": contractType, "period": period, **kwargs}
    return self.query("/futures/data/basis", params)
