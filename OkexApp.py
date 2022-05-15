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


def start():
	# websocket注册币种
	constants.INST_IDS.append(constants.Currency.BTCUSDT)
	constants.INST_IDS.append(constants.Currency.BTCUSDT_SWAP)
	# 运行websocket
	return OkexWs.run_ws_public(a_sync=True, stop_hook=out_stop_hook)


# 检查账户USDT余额
def Checkaccount(target_symbol):
	balanceresult = Accounts.balance(target_symbol)
	if len(balanceresult) != 0 and len(balanceresult[0]['details']) != 0:
		needitem = Accounts.balance(target_symbol)[0]['details'][0]
		# print(needitem)
		usdtvalue = float(needitem['cashBal'])
	else:
		usdtvalue = 0
	return usdtvalue


# 下单
def Placeorder(orders):
	info = orders[0]

	result = Orders.order(instId=info['symbol'], tdMode="cross", side=info['side'], ordType=info['type'], sz=str(info['amount']), px=str(info['price']))
	ordId = result['data'][0]['ordId']
	print(result)
	# print(ordId)
	return ordId


# 检查订单成交情况
def Checkorder(ordId, symbol):
	result = Orders.order_info(instId=symbol, ordId=ordId)
	print(result)
	fillsz = result["data"][0]["accFillSz"]
	fillpx = result["data"][0]["avgPx"]
	state = result["data"][0]["state"]
	ordersz = result["data"][0]['sz']
	orderpx = result["data"][0]['px']
	side = result["data"][0]['side']
	return fillsz, fillpx, state, ordersz, orderpx, side


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
	print("持仓信息", Accounts.positions())
	# print("账户余额", Accounts.balance())
	# print("账户余额", Accounts.balance("BTC"))
	value = Checkaccount("BTC")
	print("账户余额", value)

	# 下单/撤单
	# orders = [
	# 	{
	# 		'symbol':constants.Currency.BTCUSDT,  # 币对
	# 		'price':61000,  # 单价
	# 		'amount':0.0001,  # 数量
	# 		'type':'post_only',  # 下单类型
	# 		'side':'buy',  # 买还是卖
	# 	}
	# ]
	# id = Placeorder(orders=orders)
	# print("持仓信息", Accounts.positions())
	#
	# time.sleep(3)
	# print("撤单", Orders.cancel_order(instId=constants.Currency.BTCUSDT, clOrdId=random_order_id))
	id = "444472716903718912"
	print("订单信息", Orders.order_info(instId=constants.Currency.BTCUSDT, ordId=id))
# result = Orders.cancel_order(instId=constants.Currency.BTCUSDT, ordId=id)
# print("撤单", result)
# print("持仓信息", Accounts.positions())

# 订单信息 {'code': '0', 'data': [{'accFillSz': '0', 'avgPx': '', 'cTime': '1634134423307', 'category': 'normal', 'ccy': '', 'clOrdId': '', 'fee': '0', 'feeCcy': 'BTC', 'fillPx': '', 'fillSz': '0', 'fillTime': '', 'instId': 'BTC-USDT', 'instType': 'SPOT', 'lever': '', 'ordId': '368521713528774656', 'ordType': 'post_only', 'pnl': '0', 'posSide': 'net', 'px': '54600', 'rebate': '0', 'rebateCcy': 'USDT', 'side': 'buy', 'slOrdPx': '', 'slTriggerPx': '', 'state': 'canceled', 'sz': '0.0001', 'tag': '', 'tdMode': 'cross', 'tgtCcy': '', 'tpOrdPx': '', 'tpTriggerPx': '', 'tradeId': '', 'uTime': '1634134426337'}], 'msg': ''}
# 订单信息 {'code': '0', 'data': [{'accFillSz': '0', 'avgPx': '', 'cTime': '1635818006768', 'category': 'normal', 'ccy': '', 'clOrdId': '', 'fee': '0', 'feeCcy': 'BTC', 'fillPx': '', 'fillSz': '0', 'fillTime': '', 'instId': 'BTC-USDT', 'instType': 'SPOT', 'lever': '', 'ordId': '375583174373580801', 'ordType': 'post_only', 'pnl': '0', 'posSide': 'net', 'px': '61000', 'rebate': '0', 'rebateCcy': 'USDT', 'side': 'buy', 'slOrdPx': '', 'slTriggerPx': '', 'state': 'live', 'sz': '0.0001', 'tag': '', 'tdMode': 'cross', 'tgtCcy': '', 'tpOrdPx': '', 'tpTriggerPx': '', 'tradeId': '', 'uTime': '1635818006768'}], 'msg': ''}


# ws_thread = start()
# if ws_thread:
#     ws_thread.join()
