f"""
OKEX应用
"""
import logging

import sys
import time

import Accounts
import OkexWs
import Orders
import constants
from handlers import mkt

# API令牌信息
# utils.apikey = "ff78e819-edbc-4d3b-833e-3a149f1c58e0"
# utils.secretkey = "B06F19CB551BFBF17045143B1AC9E67F"
# utils.passPhrase = "testPassphrase"
#
# utils.apikey = "LNzrE0QaPIsehXoEL7WaGROI5jL1BkwhUzQJpcewNfLsJIcthN8V7j5OEdQR4IZ9"
# utils.secretkey = "FbsRW7e9nDgFrr1E1ZBSjrW7nG6I3qSd8nXcxCWXdNJ1tWNeo3tuoKNHEcvhoCyr"
# utils.passPhrase = 'CTA'
# utils.apikey = "kcOXZAQRWIK01pQtHLqFtkRa92cUMYC86Xjx1hNH58zLSehi3ndVal6hNbMmN15u"
# utils.secretkey = "nTnSRm1h87Qq1GKf8LfRiyE7HryXiFLaf4boX5T2voMoWx2QVwV8Ew2zxkO2qMVd"
# utils.passPhrase = "Liam"

mkt_chg = [time.time(), 0, 0, 0, 0]
def out_stop_hook():
	if mkt is None: return False
	global mkt_chg
	now_lens = [time.time(),
	            len(mkt.swap_tick_line),
	            len(mkt.spot_tick_line),
	            len(mkt.swap_trade_line),
	            len(mkt.spot_trade_line)]
	if now_lens[1] != mkt_chg[1] or now_lens[2] != mkt_chg[2] or now_lens[3] != mkt_chg[3] or now_lens[4] != mkt_chg[4]:
		mkt_chg = now_lens
	return mkt_chg[0] + 300 < time.time()

def start(out_stop_hook):
	# websocket注册币种
	constants.INST_IDS.append(constants.Currency.BTCUSDT)
	constants.INST_IDS.append(constants.Currency.BTCUSDT_SWAP)
	# 运行websocket
	return OkexWs.run_ws_public(a_sync=True, stop_hook=out_stop_hook)


# 检查账户USDT余额
def Checkaccount(target_symbol):
	balanceresult = Accounts.balance(target_symbol)
	# print(balanceresult)
	# if len(balanceresult) != 0 and len(balanceresult[0]['details']) != 0:
	# 	needitem = Accounts.balance(target_symbol)[0]['details'][0]
	# 	# print(needitem)
	# 	usdtvalue = float(needitem['cashBal'])
	# else:
	# 	usdtvalue = 0

	value = float(balanceresult[0]['balance'])

	return value


# 下单
def Placeorder(orders):
	info = orders[0]

	result = Orders.order(instId=info['symbol'], tdMode="cross", side=info['side'], ordType=info['type'], sz=str(info['amount']), px=str(info['price']))
	ordId = result['data'][0]['ordId']
	print(result)
	# print(ordId)
	return ordId


# 检查订单成交情况
def Checkorder(ordId, encodesymbol):
	result = Orders.order_info(instId=encodesymbol, ordId=ordId)
	print(result)
	fillsz = result['origQty']
	fillpx = result['avgPrice']
	state = result['status']
	ordersz = result['origQty']
	orderpx = result['avgPrice']
	side = result['side']
	return fillsz, fillpx, state, side


def Cancelorder(ordId, symbol):
	result = Orders.cancel_order(instId=symbol, ordId=ordId)
	return result


# 命令行输出级别，日志输出级别
console_print_level = logging.INFO
file_log_level = logging.DEBUG

# 日志格式配置
log_format = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
logging.basicConfig(stream=sys.stdout, level=console_print_level, format=log_format)
console_logger = logging.FileHandler(filename="OkexApp.log", mode="a", encoding="utf-8")
console_logger.setLevel(file_log_level)
console_logger.setFormatter(logging.Formatter(log_format))
logging.root.addHandler(console_logger)

if __name__ == "__main__":
	# 账户余额
	# print("账户余额", Accounts.balance())
	# print("账户余额", Accounts.balance("USDT"))
	# value = Checkaccount("USDT")
	# print(value)
	symbol = Orders.instMap(constants.Currency.BTCUSDT_SWAP)
	print("持仓信息", Accounts.positions(encodesymbol=symbol))
	exit(0)

	# 下单/撤单
	order_resp = Orders.bianOrder(__test=False, symbol=Orders.instMap('BTC-USDT-SWAP'), side='SELL', type="MARKET", quantity=0.01)
	ordId = order_resp['ordId']
	print(order_resp)

	# time.sleep(self.para_dic['waittime'])

	# 检查订单状态
	fillsz_str, fillpx_str, state_str, side_str = Checkorder(ordId=ordId, encodesymbol=Orders.instMap('BTC-USDT-SWAP'))
	print(fillsz_str)

	# time.sleep(3)
	# #print("撤单", Orders.cancel_order(instId=constants.Currency.BTCUSDT, clOrdId=random_order_id))
	# result=Orders.cancel_order(instId=constants.Currency.BTCUSDT,ordId=id)
	# print(result)

	# print("订单信息", Orders.order_info(instId=constants.Currency.BTCUSDT,ordId=id))
	# 订单信息 {'code': '0', 'data': [{'accFillSz': '0', 'avgPx': '', 'cTime': '1634134423307', 'category': 'normal', 'ccy': '', 'clOrdId': '', 'fee': '0', 'feeCcy': 'BTC', 'fillPx': '', 'fillSz': '0', 'fillTime': '', 'instId': 'BTC-USDT', 'instType': 'SPOT', 'lever': '', 'ordId': '368521713528774656', 'ordType': 'post_only', 'pnl': '0', 'posSide': 'net', 'px': '54600', 'rebate': '0', 'rebateCcy': 'USDT', 'side': 'buy', 'slOrdPx': '', 'slTriggerPx': '', 'state': 'canceled', 'sz': '0.0001', 'tag': '', 'tdMode': 'cross', 'tgtCcy': '', 'tpOrdPx': '', 'tpTriggerPx': '', 'tradeId': '', 'uTime': '1634134426337'}], 'msg': ''}
	# 订单信息 {'code': '0', 'data': [{'accFillSz': '0', 'avgPx': '', 'cTime': '1635818006768', 'category': 'normal', 'ccy': '', 'clOrdId': '', 'fee': '0', 'feeCcy': 'BTC', 'fillPx': '', 'fillSz': '0', 'fillTime': '', 'instId': 'BTC-USDT', 'instType': 'SPOT', 'lever': '', 'ordId': '375583174373580801', 'ordType': 'post_only', 'pnl': '0', 'posSide': 'net', 'px': '61000', 'rebate': '0', 'rebateCcy': 'USDT', 'side': 'buy', 'slOrdPx': '', 'slTriggerPx': '', 'state': 'live', 'sz': '0.0001', 'tag': '', 'tdMode': 'cross', 'tgtCcy': '', 'tpOrdPx': '', 'tpTriggerPx': '', 'tradeId': '', 'uTime': '1635818006768'}], 'msg': ''}
	ws_thread = start()
	if ws_thread:
		ws_thread.join()
