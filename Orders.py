f"""
订单信息
"""

import OkexRest


def order(instId: str, tdMode: str, side: str, ordType: str, sz: str, clOrdId: str = None, px: str = None,
          posSide: str = None, ccy: str = None, tag: str = None, reduceOnly: bool = None, tgtCcy: str = None):
	"""
	下单

	https://www.okex.com/docs-v5/zh/?python#rest-api-trade-place-order
	:param instId: 必填，产品ID，如 BTC-USD-190927-5000-C
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
	:param ccy: 可不填，保证金币种，仅适用于单币种保证金模式下的全仓杠杆订单
	:param clOrdId: 可不填，客户自定义订单ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。
	:param tag: 可不填，订单标签，字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-8位之间。
	:param side: 必填，订单方向
						1） buy：买
						2） sell：卖
	:param posSide: 选填，持仓方向
						1） 单向持仓模式下此参数非必填，如果填写仅可以选择
								- net
						2） 在双向持仓模式下必填，且仅可选择
								- long
								- short
							双向持仓模式下， side 和 posSide 需要进行组合
								开多：买入开多（side = buy； posSide = long ）
								开空：卖出开空（side = sell； posSide = short ）
								平多：卖出平多（side = sell；posSide = long ）
								平空：买入平空（side = buy； posSide = short ）
	:param ordType: 必填，订单类型，创建新订单时必须指定，您指定的订单类型将影响需要哪些订单参数和撮合系统如何执行您的订单，以下是有效的ordType：
						1） 普通委托：
							limit：限价单，要求指定sz 和 px
							market：市价单，币币和币币杠杆，是市价委托吃单；交割合约和永续合约，是自动以最高买/最低卖价格委托，遵循限价机制；期权合约不支持市价委托
						2） 高级委托：
							post_only：限价委托，在下单那一刻只做maker，如果该笔订单的任何部分会吃掉当前挂单深度，则该订单将被全部撤销。
							fok：限价委托，全部成交或立即取消，如果无法全部成交该笔订单，则该订单将被全部撤销。
							ioc：限价委托，立即成交并取消剩余，立即按照委托价格撮合成交，并取消该订单剩余未完成数量，不会在深度列表上展示委托数量。
							optimal_limit_ioc:市价委托，立即成交并取消剩余，仅适用于交割合约和永续合约。
	:param sz: 必填，交易数量，表示要购买或者出售的数量。
						当币币/币币杠杆以限价买入和卖出时，指交易货币数量。
						当币币/币币杠杆以市价买入时，指计价货币的数量。
						当币币/币币杠杆以市价卖出时，指交易货币的数量。
						当交割、永续、期权买入和卖出时，指合约张数。
	:param px: 选填，委托价格，仅适用于 limit：限价单、post_only：只做maker单、fok：全部成交或立即取消、ioc：立即成交并取消剩余 类型的订单
	:param reduceOnly: 可不填，只减仓
						下单时，此参数设置为 true 时，表示此笔订单具有减仓属性，只会减少持仓数量，不会增加新的持仓仓位
						仅适用于`单币种账户模式`和`跨币种账户模式`
						仅适用于`币币杠杆`，以及买卖模式下的`交割/永续`
	:param tgtCcy: 可不填，市价单委托数量的类型，仅适用于币币订单
						1) base_ccy：交易货币
						2) quote_ccy：计价货币
	"""

	order_params = {
		'instId':instId,
		'tdMode':tdMode,
		'side':side,
		'ordType':ordType,
		'sz':sz,
	}
	if clOrdId:
		order_params['clOrdId'] = clOrdId
	if px:
		order_params['px'] = px
	if posSide:
		order_params['posSide'] = posSide
	if ccy:
		order_params['ccy'] = ccy
	if tag:
		order_params['tag'] = tag
	if reduceOnly:
		order_params['reduceOnly'] = reduceOnly
	if tgtCcy:
		order_params['tgtCcy'] = tgtCcy
	return OkexRest.request_post("/api/v5/trade/order", order_params)


def cancel_order(instId, ordId=None, clOrdId=None):
	"""
	撤单
	https://www.okex.com/docs-v5/zh/?python#rest-api-trade-cancel-order

	:param instId: 产品ID，如 BTC-USD-190927-5000-C
	:param ordId: 可选，订单ID， ordId和clOrdId必须传一个，若传两个，以ordId为主
	:param clOrdId: 可选，产品ID，用户自定义ID
	"""
	order_params = {'instId':instId}
	if ordId:
		order_params['ordId'] = ordId
	elif clOrdId:
		order_params['clOrdId'] = clOrdId
	return OkexRest.request_post("/api/v5/trade/cancel-order", order_params)


def order_info(instId, ordId=None, clOrdId=None):
	"""
	订单信息
	https://www.okex.com/docs-v5/zh/?python#rest-api-trade-get-order-details

	:param instId: 产品ID ，如BTC-USD-190927
	:param ordId: 订单ID ， ordId和clOrdId必须传一个，若传两个，以ordId为主
	:param clOrdId: 用户自定义ID
	:return:
	"""
	order_params = {'instId':instId}
	if ordId:
		order_params['ordId'] = ordId
	elif clOrdId:
		order_params['clOrdId'] = clOrdId
	return OkexRest.request_get("/api/v5/trade/order", order_params)


if __name__ == '__main__':
	# result = order(instId='BTC-USDT-SWAP',tdMode='cross',side='buy',posSide='net',ordType='market',sz=str(1))
	# print(result)

	result = order(instId='BTC-USDT-SWAP', tdMode='cross', side='sell', posSide='net', ordType='market', sz=str(1))
	print(result)

# ordId = result['data'][0]['ordId']
#
# fillsz_str,fillpx_str,state_str,ordersz_str,orderpx_str,side_str = Checkorder(ordId=ordId,symbol='BTC-USDT-SWAP')
# print('fillsz_str: '+str(fillsz_str)+' fillpx_str: '+str(fillpx_str)+' state_str: '+str(state_str)+' ordersz_str: '+str(ordersz_str)+' orderpx_str: '+str(orderpx_str)+' side_str: '+str(side_str))
#
# time.sleep(2)
# result1 = order(instId='BTC-USDT-SWAP',tdMode='cross',side='sell',posSide='net',ordType='market',sz=str(1))
# print(result1)
