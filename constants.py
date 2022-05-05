class Currency(str):
	f"""
    货币
    """
	BTCUSDT = "BTC-USDT"
	BTCUSDT_SWAP = "BTC-USDT-SWAP"

	# BTCUSDT = "ETH-USDT"
	# BTCUSDT_SWAP = "ETH-USDT-SWAP"


class Operation(str):
	# 操作
	SUBSCRIBE = "subscribe"
	UNSUBSCRIBE = "unsubscribe"
	ERROR = "error"
	# 登陆
	LOGIN = "login"
	# 下单、撤单、改单相关
	ORDER = "order"
	CANCEL_ORDER = "cancel-order"
	AMEND_ORDER = "amend-order"


class Channel(str):
	f"""
    私有频道中的channel
    """
	ACCOUNT = "account"  # 账号情况
	POSITIONS = "positions"  # 持仓情况
	BALANCE_AND_POSITION = "balance_and_position"  # 账户余额和持仓频道
	ORDERS = "orders"  # 获取订单信息
	ORDERS_ALGO = "orders-algo"  # 获取策略委托订单
	f"""
    公共频道中的channel
    """
	INSTRUMENTS = "instruments"  # 产品数据
	TICKERS = "tickers"  # 产品行情
	OPEN_INTEREST = "open-interest"  # 持仓总量
	CANDLE1D = "candle1D"  # K线
	TRADES = "trades"  # 交易频道， 获取最近的成交数据
	ESTIMATED_PRICE = "estimated-price"  # 获取交割合约和期权预估交割/行权价。
	MARK_PRICE = "mark-price"  # 标记价格频道
	MARK_PRICE_CANDLE1D = "mark-price-candle1D"  # 标记价格K线频道
	PRICE_LIMIT = "price-limit"  # 限价频道, 获取交易的最高买价和最低卖价
	BOOKS = "books5"  # 深度频道
	BOOKS50 = "books50-l2-tbt"  # 深度频道
	OPT_SUMMARY = "opt-summary"  # 期权定价频道
	FUNDING_RATE = "funding-rate"  # 资金费率频道
	INDEX_CANDLE30M = "index-candle30m"  # 指数K线频道
	INDEX_TICKERS = "index-tickers"  # 指数行情频道
	STATUS = "status"  # Status 频道


INST_IDS = [Currency.BTCUSDT, Currency.BTCUSDT_SWAP]
