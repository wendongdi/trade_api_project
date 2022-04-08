f"""
订单信息
"""
from binance.futures import Futures

import utils

client = Futures(key=utils.apikey, secret=utils.secretkey, base_url=utils.api_baseurl)


def instMap(inst):
	inst = inst.replace('/', '').replace('-', '').upper()
	if inst.endswith("SWAP"): inst = inst[:-4]
	return inst


def order(instId: str, tdMode: str, side: str, ordType: str, sz: str, clOrdId: str = None, px: str = None,
          posSide: str = None, ccy: str = None, tag: str = None, reduceOnly: bool = None, tgtCcy: str = None):
	assert ccy is None and tag is None and tgtCcy is None

	if posSide:
		if posSide == 'net': posSide = 'BOTH'
		posSide = posSide.upper()

	# todo ordType
	ordType = ordType.upper()

	bares = client.new_order(symbol=instMap(instId.upper())
	                         , side=side.upper()
	                         , positionSide=posSide
	                         , type=ordType
	                         , reduceOnly=str(reduceOnly).lower()
	                         , quantity=float(sz)
	                         , price=float(px)
	                         , newClientOrderId=clOrdId
	                         , stopPrice=None
	                         , closePosition=None
	                         , activationPrice=None
	                         , callbackRate=None
	                         , timeInForce=None
	                         , workingType=None
	                         , priceProtect=None
	                         , newOrderRespType=None
	                         )

	"""
	下单

	https://www.okex.com/docs-v5/zh/?python#rest-api-trade-place-order
	:param tdMode: 必填，交易模式
						下单时需要指定
						1) 简单交易模式：
							- cash：币币和期权买方
						2) 单币种保证金模式
							- isolated：逐仓杠杆
							- cross：全仓杠杆
							- cash：全仓币币
							- cross：全仓交割/永续/期权
							- isolated：逐仓交割/永续/期权
						3) 跨币种保证金模式
							- isolated：逐仓杠杆
							- cross：全仓币币
							- cross：全仓交割/永续/期权
							- isolated：逐仓交割/永续/期权
						4) 组合保证金模式
							- isolated：逐仓杠杆
							- cross：全仓币币
							- cross：全仓交割/永续/期权
							- isolated：逐仓交割/永续/期权
	:param ordType: 必填，订单类型，创建新订单时必须指定，您指定的订单类型将影响需要哪些订单参数和撮合系统如何执行您的订单，以下是有效的ordType：
						1） 普通委托：
							limit：限价单，要求指定sz 和 px
							market：市价单，币币和币币杠杆，是市价委托吃单；交割合约和永续合约，是自动以最高买/最低卖价格委托，遵循限价机制；期权合约不支持市价委托
						2） 高级委托：
							post_only：限价委托，在下单那一刻只做maker，如果该笔订单的任何部分会吃掉当前挂单深度，则该订单将被全部撤销。
							fok：限价委托，全部成交或立即取消，如果无法全部成交该笔订单，则该订单将被全部撤销。
							ioc：限价委托，立即成交并取消剩余，立即按照委托价格撮合成交，并取消该订单剩余未完成数量，不会在深度列表上展示委托数量。
							optimal_limit_ioc:市价委托，立即成交并取消剩余，仅适用于交割合约和永续合约。
	"""

	# print(json.dumps(bares, indent=4, ensure_ascii=False))
	bares.update({
		"clOrdId":bares['clientOrderId'],
		"ordId":bares['orderId'],
		"tag":None,
		"sCode":0,
		"sMsg":''
	})
	return bares


def cancel_order(instId, ordId=None, clOrdId=None):
	bares = client.cancel_order(symbol=instMap(instId)
	                            , orderId=ordId
	                            , origClientOrderId=clOrdId
	                            )

	bares.update({
		"clOrdId":bares['clientOrderId'],
		"ordId":bares['orderId'],
		"sCode":0,
		"sMsg":''
	})
	return bares


def order_info(instId, ordId=None, clOrdId=None):
	bares = client.query_order(symbol=instMap(instId)
	                           , orderId=ordId
	                           , origClientOrderId=clOrdId
	                           )
	bares.update({
		"clOrdId":bares['clientOrderId'],
		"ordId":bares['orderId'],
		"sCode":0,
		"sMsg":''
	})
	return bares


if __name__ == '__main__':
	print(order_info('btc-usdt-swap', ordId='3022089223'))
