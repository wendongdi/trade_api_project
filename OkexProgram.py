import threading

import time

import Accounts
import OkexApp
import Orders
import handlers
import utils


class Market:
	def __init__(self):
		# 记录spot tick数据
		self.spot_tick_line = []
		self.spot_trade_line = []
		self.swap_tick_line = []
		self.swap_trade_line = []


if __name__ == '__main__':
	utils.apikey = "03af8586271056d2ed61276ec8a96be111a367bec48891a45a4ba3fce280549f"
	utils.secretkey = "d90e4114442e1fd107c1f240eef44bbf7ac0ce2eb0ce54078e270566145e3f54"
	utils.passPhrase = ""
	utils.override_api_baseurl = "https://testnet.binancefuture.com"

	# 查询
	print(Accounts.balance('usdt'))
	print(Accounts.balance('btc'))

	# 下单
	symbol = Orders.instMap("btc-usdt-swap".upper())
	order_resp = Orders.bianOrder(__test=False, symbol=symbol, side="sell".upper(), type="MARKET", positionSide=None, quantity=1, newClientOrderId="testorderid123123")
	print(order_resp)
	ordId = order_resp['ordId']
	print(Orders.order_info(symbol, ordId=ordId))

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
