f"""
订单信息
"""

import utils


def instMap(inst):
	inst = inst.replace('/', '').replace('-', '').upper()
	if inst.endswith("SWAP"): inst = inst[:-4]
	return inst


def bianOrder(symbol, side, type, positionSide=None, reduceOnly=None, quantity=None, price=None,
              newClientOrderId=None, stopPrice=None, closePosition=None, activationPrice=None,
              callbackRate=None, timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None,
              __test=False):
	"""
		币安下单接口：https://binance-docs.github.io/apidocs/futures/cn/#trade-3   \n
		参数名 参数类型 是否必填 注释    \n
		:parameter __test  BOOL    NO  测试订单请求不会实际提交 \n
		:parameter symbol	STRING	YES	交易对 \n
		:parameter side	ENUM	YES	买卖方向 SELL, BUY  \n
		:parameter type	ENUM	YES	订单类型
												LIMIT 限价单
												MARKET 市价单
												STOP_LOSS 止损单
												STOP_LOSS_LIMIT 限价止损单
												TAKE_PROFIT 止盈单
												TAKE_PROFIT_LIMIT 限价止盈单
												LIMIT_MAKER 限价只挂单
									LIMIT, MARKET, STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET    \n
									根据 order type的不同，某些参数强制要求，具体如下:    \n
									Type	强制要求的参数    \n
									LIMIT	timeInForce, quantity, price    \n
									MARKET	quantity    \n
									STOP, TAKE_PROFIT	quantity, price, stopPrice    \n
									STOP_MARKET, TAKE_PROFIT_MARKET	stopPrice    \n
									TRAILING_STOP_MARKET	callbackRate    \n
		:parameter positionSide	ENUM	NO	持仓方向，单向持仓模式下非必填，默认且仅可填BOTH;在双向持仓模式下必填,且仅可选择 LONG 或 SHORT    \n
		:parameter reduceOnly	STRING	NO	true, false; 非双开模式下默认false；双开模式下不接受此参数； 使用closePosition不支持此参数。    \n
		:parameter quantity	DECIMAL	NO	下单数量,使用closePosition不支持此参数。    \n
		:parameter price	DECIMAL	NO	委托价格    \n
		:parameter newClientOrderId	STRING	NO	用户自定义的订单号，不可以重复出现在挂单中。如空缺系统会自动赋值。必须满足正则规则 ^[\.A-Z\:/a-z0-9_-]{1,36}$    \n
		:parameter stopPrice	DECIMAL	NO	触发价, 仅 STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET 需要此参数    \n
		:parameter closePosition	STRING	NO	true, false；触发后全部平仓，仅支持STOP_MARKET和TAKE_PROFIT_MARKET；不与quantity合用；自带只平仓效果，不与reduceOnly 合用    \n
		:parameter activationPrice	DECIMAL	NO	追踪止损激活价格，仅TRAILING_STOP_MARKET 需要此参数, 默认为下单当前市场价格(支持不同workingType)    \n
		:parameter callbackRate	DECIMAL	NO	追踪止损回调比例，可取值范围[0.1, 5],其中 1代表1% ,仅TRAILING_STOP_MARKET 需要此参数    \n
		:parameter timeInForce	ENUM	NO	有效方法    \n
		:parameter workingType	ENUM	NO	stopPrice 触发类型: MARK_PRICE(标记价格), CONTRACT_PRICE(合约最新价). 默认 CONTRACT_PRICE    \n
		:parameter priceProtect	STRING	NO	条件单触发保护："TRUE","FALSE", 默认"FALSE". 仅 STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET 需要此参数    \n
		:parameter newOrderRespType	ENUM	NO	"ACK", "RESULT", 默认 "ACK"    \n
	   """

	ex_params = {}
	if positionSide: ex_params['positionSide'] = positionSide
	if reduceOnly: ex_params['reduceOnly'] = reduceOnly
	if quantity: ex_params['quantity'] = quantity
	if price: ex_params['price'] = price
	if newClientOrderId: ex_params['newClientOrderId'] = newClientOrderId
	if stopPrice: ex_params['stopPrice'] = stopPrice
	if closePosition: ex_params['closePosition'] = closePosition
	if activationPrice: ex_params['activationPrice'] = activationPrice
	if callbackRate: ex_params['callbackRate'] = callbackRate
	if timeInForce: ex_params['timeInForce'] = timeInForce
	if workingType: ex_params['workingType'] = workingType
	if priceProtect: ex_params['priceProtect'] = priceProtect
	if newOrderRespType: ex_params['newOrderRespType'] = newOrderRespType

	if __test:
		bares = utils.getFuturesClient().new_order_test(symbol, side, type, **ex_params)
	else:
		bares = utils.getFuturesClient().new_order(symbol, side, type, **ex_params)

	# print(json.dumps(bares, indent=4, ensure_ascii=False))
	bares.update({
		"clOrdId":bares['clientOrderId'],
		"ordId":bares['orderId'],
		"tag":None,
		"sCode":0,
		"sMsg":''
	})
	return bares


def order(instId: str, tdMode: str, side: str, ordType: str, sz: str, clOrdId: str = None, px: str = None,
          posSide: str = None, ccy: str = None, tag: str = None, reduceOnly: bool = None, tgtCcy: str = None):
	symbol = instMap(instId.upper())
	positionSide = posSide
	if positionSide:
		if positionSide == 'net': positionSide = 'BOTH'
		positionSide = positionSide.upper()

	# todo type & other parmas
	type = ordType.upper()

	return bianOrder(symbol=symbol, side=side.upper(), type=type, positionSide=positionSide, reduceOnly=str(reduceOnly).lower(), quantity=float(sz), price=float(px), newClientOrderId=clOrdId, stopPrice=None, closePosition=None,
	                 activationPrice=None, callbackRate=None, timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None
	                 )


def cancel_order(instId, ordId=None, clOrdId=None):
	bares = utils.getFuturesClient().cancel_order(symbol=instMap(instId), orderId=ordId, origClientOrderId=clOrdId
	                                              )

	bares.update({
		"clOrdId":bares['clientOrderId'],
		"ordId":bares['orderId'],
		"sCode":0,
		"sMsg":''
	})
	return bares


def order_info(instId, ordId=None, clOrdId=None):
	bares = utils.getFuturesClient().query_order(symbol=instMap(instId), orderId=ordId, origClientOrderId=clOrdId
	                                             )
	bares.update({
		"clOrdId":bares['clientOrderId'],
		"ordId":bares['orderId'],
		"sCode":0,
		"sMsg":''
	})
	return bares


def change_position_mode(dualSidePosition: bool):
	"""
	更改持仓模式
	:param dualSidePosition:"true": 双向持仓模式；"false": 单向持仓模式
	:return:
	"""
	return utils.getFuturesClient().change_position_mode(dualSidePosition=str(dualSidePosition).lower())


def get_position_mode(dualSidePosition: bool):
	"""
	查询持仓模式
	"""
	return utils.getFuturesClient().get_position_mode()


if __name__ == '__main__':
	print(order_info('btc-usdt-swap', ordId='3022089223'))
