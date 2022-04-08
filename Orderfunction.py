import json

import jwt
import requests

secret = 'white-test'
base_ip = 'http://3.112.57.154:8091'


# orders = [
#     {
#         'symbol': 'BTC/USDT', #币对
#         'price': 47000.4,    #单价
#         'amount': 0.0001,  # 数量
#         'type': 'ioc',  # 下单类型
#         'side': 'sell',  # 买还是卖
#     }
# ]

# 下单
def Placeorder(orders):
	body1 = {"timestamp":'12', 'orders':orders}
	encoded_jwt1 = jwt.encode(body1, secret, algorithm="HS512")
	# print(encoded_jwt1)
	headers1 = {
		'Authorization':'Bearer ' + encoded_jwt1,
		'Content-Type':'application/json;charset=utf-8'
	}
	url1 = base_ip + '/okex/createOrder'
	orders = requests.post(url1, json=body1, headers=headers1)
	print(orders.text)
	# {"data":[{"info":{"clOrdId":"","ordId":"352495406386946048","sCode":"0","sMsg":"","tag":""},"id":"352495406386946048","timestamp":1630313453934,"datetime":"2021-08-30T08:50:53.934Z","status":"open","symbol":"BTC/USDT","type":"ioc","side":"sell","price":47000.4,"amount":0.0001,"clientOrderId":"","filled":0,"remaining":0.0001,"trades":[]}],"code":0}
	if orders.text['code'] == 403:
		return 'unavailable'
	else:
		ordId = json.loads(orders.text)["data"][0]["info"]["ordId"]
		return ordId

# #检查订单成交情况
# def Checkorder(ordId,symbol):
#     body3 = {"timestamp": '12', 'orderId': ordId, 'symbol':symbol}
#     encoded_jwt3 = jwt.encode(body3, secret, algorithm="HS512")
#     #print(encoded_jwt3)
#     headers3 = {
#         'Authorization': 'Bearer ' + encoded_jwt3,
#         'Content-Type': 'application/json;charset=utf-8'
#     }
#     url3 = base_ip + '/okex/fetchOrder'
#     order = requests.get(url3, json=body3, headers=headers3)
#     #print(order.text)
#     #{"data":{"order":{"info":[{"accFillSz":"0.0001","avgPx":"47835.8","cTime":"1630318231124","category":"normal","ccy":"","clOrdId":"","fee":"-0.001195895","feeCcy":"USDT","fillPx":"47835.8","fillSz":"0.0001","fillTime":"1630318231130","instId":"BTC-USDT","instType":"SPOT","lever":"","ordId":"352515443390849026","ordType":"ioc","pnl":"0","posSide":"net","px":"47000.4","rebate":"0","rebateCcy":"BTC","side":"sell","slOrdPx":"","slTriggerPx":"","state":"filled","sz":"0.0001","tag":"","tdMode":"cross","tgtCcy":"","tpOrdPx":"","tpTriggerPx":"","tradeId":"231715357","uTime":"1630318231132"}],"clientOrderId":"","tif":""}},"code":0}
#     print(json.loads(order.text)["data"]["order"]["info"][0])
#     fillsz = json.loads(order.text)["data"]["order"]["info"][0]["accFillSz"]
#     fillpx = json.loads(order.text)["data"]["order"]["info"][0]["avgPx"]
#     state = json.loads(order.text)["data"]["order"]["info"][0]["state"]
#     ordersz = json.loads(order.text)["data"]["order"]["info"][0]['sz']
#     orderpx = json.loads(order.text)["data"]["order"]["info"][0]['px']
#     return fillsz,fillpx,state,ordersz,orderpx


# body2 = {"timestamp": '12', 'symbol': 'BTC/USDT'}
# encoded_jwt2 = jwt.encode(body2, secret, algorithm="HS512")
# print(encoded_jwt2)
# headers2 = {
#     'Authorization': 'Bearer ' + encoded_jwt2,
#     'Content-Type': 'application/json;charset=utf-8'
# }
# url2 = base_ip + '/okex/fetchPositions'
# positions = requests.get(url2, json=body2, headers=headers2)
# print(positions.text)
