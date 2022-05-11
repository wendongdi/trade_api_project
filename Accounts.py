f"""
账号信息
"""

import utils


# 账户余额
def balance(ccy=None):
	bares = utils.getFuturesClient().balance()

	# print(json.dumps(bares, indent=4, ensure_ascii=False))
	def funx(item):
		return not ccy or item['asset'] == ccy.upper()

	bares = list(filter(funx, bares))
	return bares


# 账户配置
def config():
	bares = utils.getFuturesClient().account()
	# print(json.dumps(bares, indent=4, ensure_ascii=False))
	return bares


# 账户最大可转余额
def max_withdrawal(ccy=None):
	bares = utils.getFuturesClient().balance()

	# print(json.dumps(bares, indent=4, ensure_ascii=False))
	def funx(item):
		return not ccy or item['asset'] == ccy.upper()

	bares = [{'ccy':item['asset'], 'maxWd':item['maxWithdrawAmount']} for item in list(filter(funx, bares))]
	return bares


# 查看持仓信息
def positions(instType="SWAP", instId=None, posId=None):
	"""
	:param instType:
	:param instId:
	:param posId:
	:return:
			symbol  交易对
            initialMargin   当前所需起始保证金(基于最新标记价格)
            maintMargin 维持保证金
            unrealizedProfit    持仓未实现盈亏
            positionInitialMargin   持仓所需起始保证金(基于最新标记价格)
            openOrderInitialMargin  当前挂单所需起始保证金(基于最新标记价格)
            leverage    杠杆倍率
            isolated    是否是逐仓模式
            entryPrice  持仓成本价
            maxNotional 当前杠杆下用户可用的最大名义价值
            bidNotional 买单净值，忽略
            askNotional 卖单净值，忽略
            positionSide    持仓方向
            positionAmt 持仓数量
            updateTime  更新时间

	"""

	bares = utils.getFuturesClient().account()["positions"]
	def funx(item):
		return float(item['positionAmt']) > 0 and (instId is None or item['symbol'] in instId.upper())

	def funmap(item):
		return item

	bares = [funmap(item) for item in list(filter(funx, bares))]
	return bares


if __name__ == '__main__':
	print(max_withdrawal('usdt'))
