import threading

import time

import Accounts
import OkexApp
import Orders
import handlers


class Market:
	def __init__(self):
		# 记录spot tick数据
		self.spot_tick_line = []
		self.spot_trade_line = []
		self.swap_tick_line = []
		self.swap_trade_line = []


if __name__ == '__main__':
	# utils.apikey = "LNzrE0QaPIsehXoEL7WaGROI5jL1BkwhUzQJpcewNfLsJIcthN8V7j5OEdQR4IZ9"
	# utils.secretkey = "FbsRW7e9nDgFrr1E1ZBSjrW7nG6I3qSd8nXcxCWXdNJ1tWNeo3tuoKNHEcvhoCyr"
	# utils.passPhrase = ""

	# 查询
	print(Accounts.balance('usdt'))
	print(Accounts.balance('btc'))

	# 下单
	symbol = Orders.instMap("btc-usdt-swap".upper())
	# order_resp = Orders.bianOrder(__test=True, symbol=symbol, side="sell".upper(), type="MARKET", positionSide=None, quantity=1, newClientOrderId="testorderid123123")
	# print(order_resp)
	# ordId = order_resp['ordId']
	# oinfo = Orders.order_info(symbol, ordId=ordId, clOrdId="testorderid123123")
	# print(oinfo)
	OkexApp.Checkorder(symbol=symbol,ordId="3037768141")
	# 数据
	mkt = Market()
	# 监听行情
	handlers.mkt = mkt
	# 同步锁
	handlers.books_lock = threading.Lock()
	handlers.trade_lock = threading.Lock()
	# 运行websocket
	ws_thread = OkexApp.start()

	while True:
		print(
			len(mkt.spot_trade_line),
			len(mkt.spot_tick_line),
			len(mkt.swap_trade_line),
			len(mkt.swap_tick_line)
		)
		time.sleep(3)

	if ws_thread:
		try:
			ws_thread.join()
		finally:
			pass
