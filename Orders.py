f"""
订单信息
"""
from binance.futures import Futures

import utils

client = Futures(key=utils.apikey, secret=utils.secretkey, base_url=utils.override_api_baseurl)


def instMap(inst):
	inst = inst.replace('/', '').replace('-', '').upper()
	if inst.endswith("SWAP"): inst = inst[:-4]
	return inst


def bianOrder(symbol, side, positionSide, type, reduceOnly=None, quantity=None, price=None,
              newClientOrderId=None, stopPrice=None, closePosition=None, activationPrice=None,
              callbackRate=None, timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None):
	"""
		币安下单接口：https://binance-docs.github.io/apidocs/futures/cn/#trade-3

		symbol	STRING	YES	交易对
		,side	ENUM	YES	买卖方向 SELL, BUY
		,positionSide	ENUM	NO	持仓方向，单向持仓模式下非必填，默认且仅可填BOTH;在双向持仓模式下必填,且仅可选择 LONG 或 SHORT
		,type	ENUM	YES	订单类型 LIMIT, MARKET, STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET
		,reduceOnly	STRING	NO	true, false; 非双开模式下默认false；双开模式下不接受此参数； 使用closePosition不支持此参数。
		,quantity	DECIMAL	NO	下单数量,使用closePosition不支持此参数。
		,price	DECIMAL	NO	委托价格
		,newClientOrderId	STRING	NO	用户自定义的订单号，不可以重复出现在挂单中。如空缺系统会自动赋值。必须满足正则规则 ^[\.A-Z\:/a-z0-9_-]{1,36}$
		,stopPrice	DECIMAL	NO	触发价, 仅 STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET 需要此参数
		,closePosition	STRING	NO	true, false；触发后全部平仓，仅支持STOP_MARKET和TAKE_PROFIT_MARKET；不与quantity合用；自带只平仓效果，不与reduceOnly 合用
		,activationPrice	DECIMAL	NO	追踪止损激活价格，仅TRAILING_STOP_MARKET 需要此参数, 默认为下单当前市场价格(支持不同workingType)
		,callbackRate	DECIMAL	NO	追踪止损回调比例，可取值范围[0.1, 5],其中 1代表1% ,仅TRAILING_STOP_MARKET 需要此参数
		,timeInForce	ENUM	NO	有效方法
		,workingType	ENUM	NO	stopPrice 触发类型: MARK_PRICE(标记价格), CONTRACT_PRICE(合约最新价). 默认 CONTRACT_PRICE
		,priceProtect	STRING	NO	条件单触发保护："TRUE","FALSE", 默认"FALSE". 仅 STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET 需要此参数
		,newOrderRespType	ENUM	NO	"ACK", "RESULT", 默认 "ACK"
	   """
	bares = client.new_order(symbol, side, positionSide, type
	                         , reduceOnly=reduceOnly, quantity=quantity, price=price, newClientOrderId=newClientOrderId
	                         , stopPrice=stopPrice, closePosition=closePosition, activationPrice=activationPrice
	                         , callbackRate=callbackRate, timeInForce=timeInForce, workingType=workingType
	                         , priceProtect=priceProtect, newOrderRespType=newOrderRespType
	                         )

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

	return bianOrder(symbol=symbol
	                 , side=side.upper()
	                 , positionSide=positionSide
	                 , type=type
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
