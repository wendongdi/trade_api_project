f"""
账号信息
"""
import OkexRest


# 账户余额
def balance(ccy=None):
	params = {"ccy":ccy} if ccy else {}
	return OkexRest.request_get("/api/v5/account/balance", params)['data']


# 账户配置
def config():
	return OkexRest.request_get("/api/v5/account/config")['data']


# 账户最大可转余额
def max_withdrawal(ccy=None):
	params = {"ccy":ccy} if ccy else {}
	return OkexRest.request_get("/api/v5/account/max-withdrawal", params)['data']


# 查看持仓信息
def positions(instType=None, instId=None, posId=None):
	"""
	:param instType:
	:param instId:
	:param posId:
	:return:
				instType	String	产品类型
				mgnMode	String	保证金模式
				cross：全仓
				isolated：逐仓
				posId	String	持仓ID
				posSide	String	持仓方向
				long：双向持仓多头
				short：双向持仓空头
				net：单向持仓（交割/永续/期权：pos为正代表多头，pos为负代表空头。币币杠杆：posCcy为交易货币时，代表多头；posCcy为计价货币时，代表空头。）
				pos	String	持仓数量，逐仓自主划转模式下，转入保证金后会产生pos为0的仓位
				baseBal	String	交易币余额，适用于 币币杠杆（逐仓自主划转模式）
				quoteBal	String	计价币余额 ，适用于 币币杠杆（逐仓自主划转模式）
				posCcy	String	仓位资产币种，仅适用于币币杠杆仓位
				availPos	String	可平仓数量，适用于 币币杠杆,交割/永续（开平仓模式），期权（交易账户及保证金账户逐仓）。
				avgPx	String	开仓平均价
				upl	String	未实现收益
				uplRatio	String	未实现收益率
				instId	String	产品ID，如 BTC-USD-180216
				lever	String	杠杆倍数，不适用于期权
				liqPx	String	预估强平价
				不适用于期权
				markPx	String	标记价格
				imr	String	初始保证金，仅适用于全仓
				margin	String	保证金余额，可增减，仅适用于逐仓
				mgnRatio	String	保证金率
				mmr	String	维持保证金
				liab	String	负债额，仅适用于币币杠杆
				liabCcy	String	负债币种，仅适用于币币杠杆
				interest	String	利息，已经生成的未扣利息
				tradeId	String	最新成交ID
				optVal	String	期权市值，仅适用于期权
				notionalUsd	String	以美金价值为单位的持仓数量
				adl	String	信号区
				分为5档，从1到5，数字越小代表adl强度越弱
				ccy	String	占用保证金的币种
				last	String	最新成交价
				usdPx	String	美金价格
				deltaBS	String	美金本位持仓仓位delta，仅适用于期权
				deltaPA	String	币本位持仓仓位delta，仅适用于期权
				gammaBS	String	美金本位持仓仓位gamma，仅适用于期权
				gammaPA	String	币本位持仓仓位gamma，仅适用于期权
				thetaBS	String	美金本位持仓仓位theta，仅适用于期权
				thetaPA	String	币本位持仓仓位theta，仅适用于期权
				vegaBS	String	美金本位持仓仓位vega，仅适用于期权
				vegaPA	String	币本位持仓仓位vega，仅适用于期权
				cTime	String	持仓创建时间，Unix时间戳的毫秒数格式，如 1597026383085
				uTime	String	最近一次持仓更新时间，Unix时间戳的毫秒数格式，如 1597026383085
	"""


	params = {}
	if instType: params['instType'] = instType
	if instId: params['instId'] = instId
	if posId: params['posId'] = posId
	return OkexRest.request_get("/api/v5/account/positions", params)['data']


if __name__ == '__main__':
	print(balance("BTC"))
