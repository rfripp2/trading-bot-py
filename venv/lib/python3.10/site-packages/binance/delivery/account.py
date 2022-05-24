from binance.lib.utils import check_required_parameter
from binance.lib.utils import check_required_parameters


def change_position_mode(self, dualSidePosition: str, **kwargs):
    """
    |
    | **Change Position Mode (TRADE)**
    | *Change user's position mode (Hedge Mode or One-way Mode) on EVERY symbol*

    :API endpoint: ``POST /dapi/v1/positionSide/dual``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#change-position-mode-trade

    :parameter dualSidePosition: string. "true": Hedge Mode; "false": One-way Mode.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameter(dualSidePosition, "dualSidePosition")
    params = {"dualSidePosition": dualSidePosition, **kwargs}
    url_path = "/dapi/v1/positionSide/dual"
    return self.sign_request("POST", url_path, params)


def get_position_mode(self, **kwargs):
    """
    |
    | **Get Current Position Mode (USER_DATA)**
    | *Get user's position mode (Hedge Mode or One-way Mode) on EVERY symbol*

    :API endpoint: ``GET /dapi/v1/positionSide/dual``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#get-current-position-mode-user_data

    :parameter recvWindow: optional int.
    |
    """

    params = {**kwargs}
    url_path = "/dapi/v1/positionSide/dual"
    return self.sign_request("GET", url_path, params)


def new_order(self, symbol: str, side: str, type: str, **kwargs):
    """
    |
    | **New Order (TRADE)**
    | *Send a new order*

    :API endpoint: ``POST /dapi/v1/order``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#new-order-trade

    :parameter symbol: string.
    :parameter side: string.
    :parameter type: string.
    :parameter positionSide: optional string. Default BOTH for One-way Mode; LONG or SHORT for Hedge Mode. It must be passed in Hedge Mode.
    :parameter timeInForce: optional string.
    :parameter quantity: optional float.
    :parameter reduceOnly: optional string.
    :parameter price: optional float.
    :parameter newClientOrderId: optional string. An unique ID among open orders. Automatically generated if not sent.
    :parameter stopPrice: optional float. Use with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders.
    :parameter closePosition: optional string. true or false; Close-All, use with STOP_MARKET or TAKE_PROFIT_MARKET.
    :parameter activationPrice: optional float. Use with TRAILING_STOP_MARKET orders, default is the latest price (supporting different workingType).
    :parameter callbackRate: optional float. Use with TRAILING_STOP_MARKET orders, min 0.1, max 5 where 1 for 1%.
    :parameter workingType: optional string. stopPrice triggered by: "MARK_PRICE", "CONTRACT_PRICE". Default "CONTRACT_PRICE".
    :parameter priceProtect: optional string. "TRUE" or "FALSE", default "FALSE". Use with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders.
    :parameter newOrderRespType: optional float. "ACK" or "RESULT", default "ACK".
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameters([[symbol, "symbol"], [side, "side"], [type, "type"]])
    params = {"symbol": symbol, "side": side, "type": type, **kwargs}
    url_path = "/dapi/v1/order"
    return self.sign_request("POST", url_path, params)


def modify_order(self, symbol: str, side: str, **kwargs):
    """
    |
    | **Modify Order (TRADE)**
    | *Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue.*

    :API endpoint: ``POST /dapi/v1/order``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#modify-order-trade

    :parameter symbol: string.
    :parameter side: string.
    :parameter orderId: optional int. Either orderId or origClientOrderId must be sent, and the orderId will prevail if both are sent.
    :parameter origClientOrderId: optional string.
    :parameter quantity: optional float.
    :parameter price: optional float. Either quantity or price must be sent.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameters([[symbol, "symbol"], [side, "side"]])
    params = {"symbol": symbol, "side": side, **kwargs}
    url_path = "/dapi/v1/order"
    return self.sign_request("PUT", url_path, params)


def new_batch_order(self, batchOrders: list):
    """
    |
    | **Place Multiple Orders (TRADE)**

    :API endpoint: ``POST /dapi/v1/batchOrders``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#place-multiple-orders-trade

    :parameter batchOrders: list. Order list, max 5 orders.
    :parameter recvWindow: optional int.
    |
    """

    params = {"batchOrders": batchOrders}
    url_path = "/dapi/v1/batchOrders"
    return self.sign_request("POST", url_path, params, True)


def modify_batch_order(self, batchOrders: list):
    """
    |
    | **Modify Multiple Orders (TRADE)**

    :API endpoint: ``PUT /dapi/v1/batchOrders``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#modify-multiple-orders-trade

    :parameter batchOrders: list. Order list, max 5 orders
    :parameter recvWindow: optional int.
    |
    """

    params = {"batchOrders": batchOrders}
    url_path = "/dapi/v1/batchOrders"
    return self.sign_request("PUT", url_path, params)


def order_modify_history(self, symbol: str, **kwargs):
    """
    |
    | **Get Order Modify History (USER_DATA)**
    | *Get order modification history*

    :API endpoint: ``GET /dapi/v1/orderAmendment``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#get-order-modify-history-user_data

    :parameter symbol: string.
    :parameter orderId: optional int.
    :parameter origClientOrderId: optional string. Either orderId or origClientOrderId must be sent, and the orderId will prevail if both are sent.
    :parameter startTime: optional int. Timestamp in ms to get modification history from INCLUSIVE.
    :parameter endTime: optional int. Timestamp in ms to get modification history until INCLUSIVE.
    :parameter limit: optional int.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/dapi/v1/orderAmendment"
    return self.sign_request("GET", url_path, params)


def query_order(self, symbol: str, **kwargs):
    """
    |
    | **Query Order (USER_DATA)**
    | *Check an order's status.*

    :API endpoint: ``GET /dapi/v1/order``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#query-order-user_data

    :parameter symbol: string.
    :parameter orderId: optional string.
    :parameter origClientOrderId: optional string. Either orderId or origClientOrderId must be sent.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/dapi/v1/order"
    return self.sign_request("GET", url_path, params)


def cancel_order(self, symbol: str, **kwargs):
    """
    |
    | **Cancel Order (TRADE)**
    | *Cancel an active order.*

    :API endpoint: ``DELETE /dapi/v1/order``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#cancel-order-trade

    :parameter symbol: string.
    :parameter orderId: optional string.
    :parameter origClientOrderId: optional string.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/dapi/v1/order"
    return self.sign_request("DELETE", url_path, params)


def cancel_open_orders(self, symbol: str, **kwargs):
    """
    |
    | **Cancel All Open Orders (TRADE)**

    :API endpoint: ``DELETE /dapi/v1/allOpenOrders``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#cancel-all-open-orders-trade

    :parameter symbol: string.
    :parameter recvWindow: optional int.
    |
    """
    
    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/dapi/v1/allOpenOrders"
    return self.sign_request("DELETE", url_path, params)


def cancel_batch_order(self, symbol: str, **kwargs):
    """
    |
    | **Cancel Multiple Orders (TRADE)**

    :API endpoint: ``DELETE /dapi/v1/batchOrders``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#cancel-multiple-orders-trade

    :parameter symbol: string.
    :parameter orderIdList: optional int list. Max length 10 e.g. [1234567,2345678]
    :parameter origClientOrderIdList: optional string list. Max length 10 e.g. ["my_id_1","my_id_2"], encode the double quotes. No space after comma. Either orderIdList or origClientOrderIdList must be sent.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/dapi/v1/batchOrders"
    return self.sign_request("DELETE", url_path, params)


def countdown_cancel_order(self, symbol: str, countdownTime: int, **kwargs):
    """
    |
    | **Auto-Cancel All Open Orders (TRADE)**
    | *Cancel all open orders of the specified symbol at the end of the specified countdown.*

    :API endpoint: ``POST /dapi/v1/countdownCancelAll``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#auto-cancel-all-open-orders-trade

    :parameter symbol: string.
    :parameter countdownTime: int list. Countdown time, 1000 for 1 second. 0 to cancel the timer.
    :parameter recvWindow: optional int.
    |
    """
    
    check_required_parameters([[symbol, "symbol"], [countdownTime, "countdownTime"]])
    params = {"symbol": symbol, "countdownTime": countdownTime, **kwargs}
    url_path = "/dapi/v1/countdownCancelAll"
    return self.sign_request("POST", url_path, params)


def get_open_orders(self, symbol: str, orderId: int = None, origClientOrderId: str = None, **kwargs):
    """
    |
    | **Query Current Open Order (USER_DATA)**

    :API endpoint: ``GET /dapi/v1/openOrder``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#query-current-open-order-user_data

    :parameter symbol: string.
    :parameter orderId: optional string.
    :parameter origClientOrderId: optional string. EitherorderId or origClientOrderId must be sent.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/dapi/v1/openOrder"
    return self.sign_request("GET", url_path, params)


def get_orders(self, **kwargs):
    """
    |
    | **Current All Open Orders (USER_DATA)**
    | *Get all open orders on a symbol. Careful when accessing this with no symbol.*
    | *If the symbol is not sent, orders for all symbols will be returned in an array.*

    :API endpoint: ``GET /dapi/v1/openOrders``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#current-all-open-orders-user_data

    :parameter symbol: optional string.
    :parameter recvWindow: optional int.
    |
    """

    params = { **kwargs }
    url_path = "/dapi/v1/openOrders"
    return self.sign_request("GET", url_path, params)


def get_all_orders(self, **kwargs):
    """
    |
    | **All Orders (USER_DATA)**
    | *Get all account orders; active, canceled, or filled.*

    :API endpoint: ``GET /dapi/v1/allOrders``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#all-orders-user_data

    :parameter symbol: optional string.
    :parameter pair: optional string.
    :parameter orderId: optional int.
    :parameter startTime: optional int
    :parameter endTime: optional int
    :parameter limit: optional int. Default 50, max 100.
    :parameter recvWindow: optional int.
    |
    """
    
    params = {**kwargs}
    url_path = "/dapi/v1/allOrders"
    return self.sign_request("GET", url_path, params)


def balance(self, **kwargs):
    """
    |
    | **Futures Account Balance (USER_DATA)**

    :API endpoint: ``GET /dapi/v1/balance``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#futures-account-balance-user_data

    :parameter recvWindow: optional int
    |
    """

    url_path = "/dapi/v1/balance"
    return self.sign_request("GET", url_path, {**kwargs})


def account(self, **kwargs):
    """
    |
    | **Account Information (USER_DATA)**
    | *Get current account information*

    :API endpoint: ``GET /dapi/v1/account``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#account-information-user_data

    :parameter recvWindow: optional int
    |
    """

    url_path = "/dapi/v1/account"
    return self.sign_request("GET", url_path, {**kwargs})


def change_leverage(self, symbol: str, leverage: int, **kwargs):
    """
    |
    | **Change Initial Leverage (TRADE)**
    | *Change user's initial leverage in the specific symbol market.*
    | *For Hedge Mode, LONG and SHORT positions of one symbol use the same initial leverage and share a total notional value.*

    :API endpoint: ``POST /dapi/v1/leverage``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#change-initial-leverage-trade

    :parameter symbol: string.
    :parameter leverage: int. Target initial leverage: int from 1 to 125.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameters([[symbol, "symbol"],[leverage, "leverage"]])
    params = {"symbol": symbol, "leverage": leverage, **kwargs}
    url_path = "/dapi/v1/leverage"
    return self.sign_request("POST", url_path, params)


def change_margin_type(self, symbol: str, marginType: str, **kwargs):
    """
    |
    | **Change Margin Type (TRADE)**
    | *Change user's margin type in the specific symbol market.For Hedge Mode, LONG and SHORT positions of one symbol use the same margin type.*
    | *With ISOLATED margin type, margins of the LONG and SHORT positions are isolated from each other.*

    :API endpoint: ``POST /dapi/v1/marginType``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#change-margin-type-trade

    :parameter symbol: string.
    :parameter leverage: string. ISOLATED, CROSSED.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameters([[symbol, "symbol"],[marginType, "marginType"]])
    params = {"symbol": symbol, "marginType": marginType, **kwargs}
    url_path = "/dapi/v1/marginType"
    return self.sign_request("POST", url_path, params)


def modify_isolated_position_margin(self, symbol: str, amount: float, type: int, **kwargs):
    """
    |
    | **Modify Isolated Position Margin (TRADE)**

    :API endpoint: ``POST /dapi/v1/positionMargin``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#modify-isolated-position-margin-trade

    :parameter symbol: string.
    :parameter amount: float.
    :parameter type: int. 1: Add position margin, 2: Reduce position margin
    :parameter positionSide: optional string. Default BOTH for One-way Mode, LONG or SHORT for Hedge Mode. It must be sent with Hedge Mode.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameters([[symbol, "symbol"], [amount, "amount"], [type, "type"]])
    params = {"symbol": symbol, "amount": amount, "type": type, **kwargs}
    url_path = "/dapi/v1/positionMargin"
    return self.sign_request("POST", url_path, params)


def get_position_margin_history(self, symbol: str, **kwargs):
    """
    |
    | **Get Position Margin Change History (TRADE)**

    :API endpoint: ``GET /dapi/v1/positionMargin/history``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#get-position-margin-change-history-trade

    :parameter symbol: string.
    :parameter type: optional int. 1: Add position margin, 2: Reduce position margin
    :parameter startTime: optional string.
    :parameter endTime: optional string.
    :parameter limit: optional int. Default 50.
    :parameter recvWindow: optional int.
    |
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/dapi/v1/positionMargin/history"
    return self.sign_request("GET", url_path, params)


def get_position_risk(self, **kwargs):
    """
    |
    | **Position Information (USER_DATA)**
    | *Get current position information.*

    :API endpoint: ``GET /dapi/v1/positionRisk``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#position-information-user_data

    :parameter marginAsset: optional string.
    :parameter pair: optional string. If neither marginAsset nor pair is sent, positions of all symbols with TRADING status will be returned.
    :parameter recvWindow: optional int.
    |
    """

    params = {**kwargs}
    url_path = "/dapi/v1/positionRisk"
    return self.sign_request("GET", url_path, params)


def get_account_trades(self, **kwargs):
    """
    |
    | **Account Trade List (USER_DATA)**
    | *Get trades for a specific account and symbol.*

    :API endpoint: ``GET /dapi/v1/userTrades``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#account-trade-list-user_data

    :parameter symbol: optional string.
    :parameter pair: optional string.
    :parameter startTime: optional string.
    :parameter endTime: optional string.
    :parameter fromId: optional int. Trade ID to fetch from, default is to get the most recent trades.
    :parameter limit: optional int. Default 50, max 100.
    :parameter recvWindow: optional int.
    |
    """

    params = {**kwargs}
    url_path = "/dapi/v1/userTrades"
    return self.sign_request("GET", url_path, params)


def get_income_history(self, **kwargs):
    """
    |
    | **Get Income History (USER_DATA)**

    :API endpoint: ``GET /dapi/v1/income``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#get-income-history-user_data

    :parameter symbol: optional string.
    :parameter incomeType: optional string. "TRANSFER", "WELCOME_BONUS", "REALIZED_PNL", "FUNDING_FEE", "COMMISSION" and "INSURANCE_CLEAR"
    :parameter startTime: optional string. Timestamp in ms to get funding from INCLUSIVE.
    :parameter endTime: optional string. timestamp in ms to get funding until INCLUSIVE.
    :parameter limit: optional int. Default 100, max 100.
    :parameter recvWindow: optional int.
    |
    """

    params = {**kwargs}
    url_path = "/dapi/v1/income"
    return self.sign_request("GET", url_path, params)


def leverage_brackets(self, symbol: str = None, pair: str = None, **kwargs):
    """
    |
    | **Notional Bracket for Symbol(USER_DATA)**
    | *Get the pair's default notional bracket list.*

    :API endpoint: ``GET /dapi/v1/leverageBracket``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#notional-bracket-for-pair-user_data

    :API endpoint: ``GET /dapi/v2/leverageBracket``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#notional-bracket-for-pair-user_data-2

    :parameter symbol: optional string.
    :parameter pair: optional string.
    :parameter recvWindow: optional int.
    |
    """

    url_path = ""
    params = {}

    if (symbol is None) and (pair is None):
        url_path = "/dapi/v2/leverageBracket"
        params = {**kwargs}
    elif (symbol is None):
        url_path = "/dapi/v2/leverageBracket"
        params = {"symbol": symbol, **kwargs}
    else:
        url_path = "/dapi/v1/leverageBracket"
        params = {"pair": pair,  **kwargs}

    return self.sign_request("GET", url_path, params)


def adl_quantile(self, **kwargs):
    """
    |
    | **Position ADL Quantile Estimation (USER_DATA)**

    :API endpoint: ``GET /dapi/v1/adlQuantile``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#position-adl-quantile-estimation-user_data

    :parameter symbol: optional string.
    :parameter recvWindow: optional int.
    |
    """

    params = {**kwargs}
    url_path = "/dapi/v1/adlQuantile"
    return self.sign_request("GET", url_path, params)


def force_orders(self, **kwargs):
    """
    |
    | **User's Force Orders (USER_DATA)**

    :API endpoint: ``GET /dapi/v1/forceOrders``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#user-39-s-force-orders-user_data

    :parameter symbol: optional string.
    :parameter autoCloseType: optional string "LIQUIDATION" for liquidation orders, "ADL" for ADL orders.
    :parameter startTime: optional string.
    :parameter endTime: optional string.
    :parameter limit: optional int. Default 50, max 100.
    :parameter recvWindow: optional int.
    |
    """

    params = {**kwargs}
    url_path = "/dapi/v1/forceOrders"
    return self.sign_request("GET", url_path, params)


def commission_rate(self, symbol: str, **kwargs):
    """
    |
    | **User Commission Rate (USER_DATA)**

    :API endpoint: ``GET /dapi/v1/commissionRate``
    :API doc: https://binance-docs.github.io/apidocs/delivery/en/#user-commission-rate-user_data

    :parameter symbol: optional string.
    :parameter recvWindow: optional int.
    |
    """
    
    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    url_path = "/dapi/v1/commissionRate"
    return self.sign_request("GET", url_path, params)
