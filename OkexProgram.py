import threading
import time

import OkexApp
import handlers


class Market:
	def __init__(self):
		# 记录spot tick数据
		self.spot_tick_line = []
		self.spot_trade_line = []
		self.swap_tick_line = []
		self.swap_trade_line = []


if __name__ == '__main__':
	mkt = Market()
	# 监听行情
	handlers.mkt = mkt
	# 同步锁
	handlers.books_lock = threading.Lock()
	handlers.trade_lock = threading.Lock()
	# 运行websocket

	ws_thread = OkexApp.start()
	if ws_thread:
		try:
			ws_thread.join()
		finally:
			pass
