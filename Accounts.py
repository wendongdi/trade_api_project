f"""
账号信息
"""

from binance.futures import Futures

import utils

client = Futures(key=utils.apikey, secret=utils.secretkey, base_url=utils.api_baseurl)


# 账户余额
def balance(ccy=None):
	bares = client.balance()

	# print(json.dumps(bares, indent=4, ensure_ascii=False))
	def funx(item):
		return not ccy or item['asset'] == ccy.upper()

	bares = list(filter(funx, bares))
	return bares


# 账户配置
def config():
	bares = client.account()
	# print(json.dumps(bares, indent=4, ensure_ascii=False))
	return bares


# 账户最大可转余额
def max_withdrawal(ccy=None):
	bares = client.balance()

	# print(json.dumps(bares, indent=4, ensure_ascii=False))
	def funx(item):
		return not ccy or item['asset'] == ccy.upper()

	bares = [{'ccy':item['asset'], 'maxWd':item['maxWithdrawAmount']} for item in list(filter(funx, bares))]
	return bares


if __name__ == '__main__':
	print(max_withdrawal('usdt'))
