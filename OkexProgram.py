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
	# utils.apikey = "LNzrE0QaPIsehXoEL7WaGROI5jL1BkwhUzQJpcewNfLsJIcthN8V7j5OEdQR4IZ9"
	# utils.secretkey = "FbsRW7e9nDgFrr1E1ZBSjrW7nG6I3qSd8nXcxCWXdNJ1tWNeo3tuoKNHEcvhoCyr"
	# utils.passPhrase = ""

	# 查询
	# print(Accounts.balance('usdt'))
	# print(Accounts.balance('btc'))

	# 下单
	# symbol = Orders.instMap("btc-usdt-swap".upper())
	# order_resp = Orders.bianOrder(__test=True, symbol=symbol, side="sell".upper(), type="MARKET", positionSide=None, quantity=1, newClientOrderId="testorderid123123")
	# print(order_resp)
	# ordId = order_resp['ordId']
	# oinfo = Orders.order_info(symbol, ordId=ordId, clOrdId="testorderid123123")
	# print(oinfo)
	# OkexApp.Checkorder(encodesymbol=symbol,ordId="3037768141")
	# 数据
	mkt = Market()
	# 监听行情
	handlers.mkt = mkt
	# 同步锁
	handlers.books_lock = threading.Lock()
	handlers.trade_lock = threading.Lock()
	# 运行websocket
	ws_thread = OkexApp.start()

	time.sleep(5)

	lindx = 0

	while True:
		if len(mkt.swap_tick_line) - 1 > lindx:
			lindx = len(mkt.swap_tick_line) - 1
			print(mkt.swap_tick_line[lindx])
		continue
		for lines in [mkt.spot_tick_line, mkt.swap_tick_line]:

			if len(lines) < 2: continue

			indx = len(lines) - 1
			last_0, lines_0 = lines[indx], lines[:indx]
			dups = []
			for line_0 in lines_0:
				if not handlers.not_dup_check(line_0, last_0):
					dups.append(line_0)
			for dup in dups:
				dup_secs = (float(last_0['timestamp']) - float(dup['timestamp'])) / 1000.0
				print(dup_secs, last_0, dup)

	#
	# while True:
	# 	close_check_logs = {}
	# 	for i in range(2):
	# 		spot_last = mkt.spot_tick_line[-1]
	# 		spot_close = (spot_last['ask_0_p'] + spot_last['bid_0_p']) / 2
	# 		swap_last = mkt.swap_tick_line[-1]
	# 		swap_close = (swap_last['ask_0_p'] + swap_last['bid_0_p']) / 2
	# 		ckey = (spot_close, swap_close)
	# 		if ckey not in close_check_logs:
	# 			close_check_logs[ckey] = []
	# 		close_check_logs[ckey].append((spot_last, swap_last))
	# 		time.sleep(60)
	# 	for k,v in close_check_logs.items():
	# 		if len(v) > 1:
	# 			print(k)
	# 			print(v)
	# 			print()

	if ws_thread:
		try:
			ws_thread.join()
		finally:
			pass
