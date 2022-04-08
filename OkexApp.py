f"""
OKEX应用
"""
import logging
import sys

import Accounts
import OkexWs
import Orders
import constants
import strategies

# API令牌信息
# utils.apikey = "ff78e819-edbc-4d3b-833e-3a149f1c58e0"
# utils.secretkey = "B06F19CB551BFBF17045143B1AC9E67F"
# utils.passPhrase = "testPassphrase"

# utils.apikey = '260705c5-a7b4-4c47-87d5-6982b9ac3370'
# utils.secretkey = '0CEF5002C71E0DA7725EA71DAF89C4CE'
# utils.passPhrase = 'Cm2355'

# utils.apikey = "ea028e9c-3eb9-4ca8-a27e-e2b2db270609"
# utils.secretkey = "B17D67D2E73F069B559DB82A053BCB27"
# utils.passPhrase = 'Cm2355'


# 命令行输出级别，日志输出级别
console_print_level = logging.INFO
file_log_level = logging.WARN

# 日志格式配置
log_format = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
logging.basicConfig(stream=sys.stdout, level=console_print_level, format=log_format)
console_logger = logging.FileHandler(filename="OkexApp.log", mode="a", encoding="utf-8")
console_logger.setLevel(file_log_level)
console_logger.setFormatter(logging.Formatter(log_format))
logging.root.addHandler(console_logger)


def start():
	# websocket注册币种
	strategies.WsPublicStrategy.INST_IDS.append(constants.Currency.BTCUSDT)
	strategies.WsPublicStrategy.INST_IDS.append(constants.Currency.BTCUSDT_SWAP)
	# 运行websocket
	return OkexWs.run_ws_public(a_sync=True)


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


if __name__ == "__main__":
	ws_thread = start()

	# 账户余额
	# print("账户余额", Accounts.balance())
	# print("账户余额", Accounts.balance("BTC"))
	value = Checkaccount()
	print(value)

# 下单/撤单
# fake = Faker("zh-CN")
# random_order_id = fake.pystr(min_chars=1, max_chars=32)
# print("下单", Orders.order(instId=constants.Currency.BTCUSDT,
#                          tdMode="cross", side="buy",
#                          ordType="ioc", sz="0.0001", px="54800"))

# orders = [
#     {
#         'symbol': constants.Currency.BTCUSDT, #币对
#         'price': 61000,    #单价
#         'amount': 0.0001,  # 数量
#         'type': 'post_only',  # 下单类型
#         'side': 'buy',  # 买还是卖
#     }
# ]
# id = Placeorder(orders=orders)
# print(id)

# time.sleep(3)
# #print("撤单", Orders.cancel_order(instId=constants.Currency.BTCUSDT, clOrdId=random_order_id))
# result=Orders.cancel_order(instId=constants.Currency.BTCUSDT,ordId=id)
# print(result)

# print("订单信息", Orders.order_info(instId=constants.Currency.BTCUSDT,ordId=id))
# 订单信息 {'code': '0', 'data': [{'accFillSz': '0', 'avgPx': '', 'cTime': '1634134423307', 'category': 'normal', 'ccy': '', 'clOrdId': '', 'fee': '0', 'feeCcy': 'BTC', 'fillPx': '', 'fillSz': '0', 'fillTime': '', 'instId': 'BTC-USDT', 'instType': 'SPOT', 'lever': '', 'ordId': '368521713528774656', 'ordType': 'post_only', 'pnl': '0', 'posSide': 'net', 'px': '54600', 'rebate': '0', 'rebateCcy': 'USDT', 'side': 'buy', 'slOrdPx': '', 'slTriggerPx': '', 'state': 'canceled', 'sz': '0.0001', 'tag': '', 'tdMode': 'cross', 'tgtCcy': '', 'tpOrdPx': '', 'tpTriggerPx': '', 'tradeId': '', 'uTime': '1634134426337'}], 'msg': ''}
# 订单信息 {'code': '0', 'data': [{'accFillSz': '0', 'avgPx': '', 'cTime': '1635818006768', 'category': 'normal', 'ccy': '', 'clOrdId': '', 'fee': '0', 'feeCcy': 'BTC', 'fillPx': '', 'fillSz': '0', 'fillTime': '', 'instId': 'BTC-USDT', 'instType': 'SPOT', 'lever': '', 'ordId': '375583174373580801', 'ordType': 'post_only', 'pnl': '0', 'posSide': 'net', 'px': '61000', 'rebate': '0', 'rebateCcy': 'USDT', 'side': 'buy', 'slOrdPx': '', 'slTriggerPx': '', 'state': 'live', 'sz': '0.0001', 'tag': '', 'tdMode': 'cross', 'tgtCcy': '', 'tpOrdPx': '', 'tpTriggerPx': '', 'tradeId': '', 'uTime': '1635818006768'}], 'msg': ''}

# if ws_thread:
#     ws_thread.join()
