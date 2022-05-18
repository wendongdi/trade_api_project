f"""
消息处理
"""
import logging
import operator
import random
import threading

import time

import Books
import Instruments
from constants import Currency
from utils import HeaderUtils

console_print_level = logging.INFO
file_log_level = logging.WARNING

mkt = None
books_lock: threading.Lock
trade_lock: threading.Lock
tick_lock = threading.Lock()


def err_handle(json_msg):
	logging.error(f"异常响应消息\t{json_msg}")


def common_handle(json_msg):
	logging.warning(f"通常响应消息\t{json_msg}")


def data_common_handle(instId, datas):
	logging.warning(f"通常推送消息\t{instId, datas}")


def instruments_handle(ingore_1, datas):
	for data in datas:
		if data["instId"]:
			instId = data["instId"]
			logging.debug(f"产品更新推送消息\t{instId, data}")
			if data['ctVal']:
				Instruments.CtVals[data["instId"]] = float(data['ctVal'])


def subscribe_handle(json_msg):
	logging.info(f"订阅响应消息\t{json_msg}")


# def tick_handle_proxy(instId: str, datas):
# 	cd = 0
# 	while tick_lock.locked():
# 		if random.randint(0, 120) < 1: logging.warning(f"tick_handle_proxy[{cd}] 等待tick_lock")
# 		cd += 1
# 		time.sleep(0.1)
# 	tick_lock.acquire()
# 	try:
# 		tick_handle(instId, datas)
# 	finally:
# 		tick_lock.release()


def books_handle_proxy(instId: str, datas):
	cd = 0
	while books_lock.locked():
		if random.randint(0, 120) < 1: logging.warning(f"books_handle_proxy[{cd}] 等待books_lock")
		cd += 1
		time.sleep(0.1)
	books_lock.acquire()
	try:
		books_handle(instId, datas)
	finally:
		books_lock.release()


def trade_handle_proxy(instId: str, datas):
	cd = 0
	while trade_lock.locked():
		if random.randint(0, 120) < 1: logging.warning(f"trade_handle_proxy[{cd}] 等待trade_lock")
		cd += 1
		time.sleep(0.1)
	trade_lock.acquire()
	try:
		trade_handle(instId, datas)
	finally:
		trade_lock.release()


# def tick_handle(instId: str, datas):
# 	"""
# 	行情频道推送
# 	:param instId: 产品ID
# 	:param datas: 数据
# 					instType 产品类型
# 					instId 产品ID
# 					last 最新成交价
# 					lastSz 最新成交的数量
# 					askPx 卖一价
# 					askSz 卖一价对应的量
# 					bidPx 买一价
# 					bidSz 买一价对应的数量
# 					vol24h 24小时成交量，以张为单位
# 					volCcy24h 24小时成交量，以币为单位
# 					open24h 24小时开盘价
# 					high24h 24小时最高价
# 					low24h 24小时最低价
# 					sodUtc0 UTC 0 时开盘价
# 					sodUtc8 UTC+8 时开盘价
# 					ts 数据更新时间戳
# 	:return:
# 	"""
# 	logging.debug(f"行情频道推送消息\t{instId}\t{datas}")
# 	for data in datas:
# 		assert data['instId'] == instId
# 		is_swap = instId.endswith("-SWAP")
# 		if is_swap:
# 			ctVal = Instruments.ctVal("SWAP", instId)
# 			data["lastSz"] = str(int(data["lastSz"]) * ctVal)
# 			data["askSz"] = str(int(data["askSz"]) * ctVal)
# 			data["bidSz"] = str(int(data["bidSz"]) * ctVal)
# 		# todo 在此处理实时行情数据
# 		item_unix_ts = int(data['ts'])
# 		local_unix_ts = HeaderUtils.get_unix_timestamp_ns()
# 		data['timestamp'] = item_unix_ts
# 		data['exchange'] = 'okex'
# 		data['asset_type'] = 'swap' if is_swap else 'spot'
# 		data['symbol'] = instId
# 		data['local_timestamp'] = local_unix_ts
# 		data['time'] = HeaderUtils.get_timestamp(item_unix_ts, False)
# 		data['local_time'] = HeaderUtils.get_timestamp(local_unix_ts, False)
# if instId == Currency.BTCUSDT:
#     Market.spot_tick_line.append(data)
# elif instId == Currency.BTCUSDT_SWAP:
#     Market.swap_tick_line.append(data)


local_ts_cache = {

}


def trade_handle(instId: str, datas, source_type="推送"):
	"""
	交易频道推送
	:param instId: 产品ID
	:param datas: 数据
					instId 产品ID
					tradeId 成交ID
					px 成交价格
					sz 成交数量
					side 成交方向
					ts 数据更新时间戳
	:return:
	"""
	logging.debug(f"交易频道推送消息\t{instId}\t{datas}")
	for data in datas:
		item_unix_ts = int(data['ts'])
		# local_ts_key = 'trade_'+instId
		# if local_ts_key in local_ts_cache and local_ts_cache[local_ts_key][0] >= item_unix_ts:
		#     logging.error([local_ts_key, source_type, "时间顺序错误 local={} remote={}".format(local_ts_cache[local_ts_key],item_unix_ts)])
		#     return
		assert data['instId'] == instId
		is_swap = instId.endswith("-SWAP")
		if is_swap:
			ctVal = Instruments.ctVal("SWAP", instId)
			data["sz"] = str(int(data["sz"]) * ctVal)
		# todo 在此处理实时行情数据
		# trade数据格式{'timestamp': 1631029687865, 'local_timestamp': 1631029689725, 'exchange': 'okex', 'asset_type': 'spot', 'symbol': 'BTC/USDT', 'id': '236019027', 'side': 'buy', 'price': 46783.6, 'amount': 1e-05, 'time': '2021-09-07T15:48:07.865000Z', 'local_time': '2021-09-07T15:48:09.725000Z'}
		local_unix_ts = HeaderUtils.get_unix_timestamp_ns()
		data['timestamp'] = item_unix_ts
		data['exchange'] = 'okex'
		data['asset_type'] = 'swap' if is_swap else 'spot'
		data['symbol'] = instId
		data['local_timestamp'] = local_unix_ts
		data['id'] = int(data['tradeId'])
		data['price'] = float(data['px'])
		data['amount'] = float(data['sz'])
		data['time'] = HeaderUtils.get_timestamp(item_unix_ts, False)
		data['local_time'] = HeaderUtils.get_timestamp(local_unix_ts, False)
		logging.debug(data)
		# local_ts_cache[local_ts_key] = (item_unix_ts,data)
		if instId == Currency.BTCUSDT:
			line_append(mkt.spot_trade_line, data)
		elif instId == Currency.BTCUSDT_SWAP:
			line_append(mkt.swap_trade_line, data)


limit_ts = 0


def books_handle(instId, datas, source_type="推送"):
	global limit_ts
	change_count = 0

	def update(new_ts: int, new_asks, new_bids):
		Books.tss[instId] = new_ts
		Books.books_data[instId]['asks'] = new_asks
		Books.books_data[instId]['bids'] = new_bids

	logging.debug(f"深度频道推送消息\t{instId}\t{datas}")
	if len(datas) < 1: return
	data = datas[0]
	ts: int = int(data['ts'])
	if Books.tss[instId] >= ts:
		return
	else:
		incr_asks = data['asks']
		incr_bids = data['bids']
		if 'checksum' in data:
			if Books.tss[instId] <= 0 or len(Books.books_data[instId]['bids']) < 50 or len(Books.books_data[instId]['asks']) < 50:
				Books.force_update(instId)
				change_count += 1
			source_type = "增量推送"
			checksum = data['checksum']
			all_bids, b_change_count = Books.update_bids(incr_bids, Books.books_data[instId]['bids']), 1
			all_asks, a_change_count = Books.update_asks(incr_asks, Books.books_data[instId]['asks']), 1
			change_count += (b_change_count + a_change_count)
			if change_count <= 0:
				return
			check_num = Books.check(all_bids, all_asks)
			if checksum != check_num or len(all_bids) < 20 or len(all_asks) < 20:
				if time.time() > limit_ts:
					# 限制接口调用频次
					limit_ts = time.time() + 0.15
					logging.debug(f"合并深度数据未通过校验\t{instId}\t{checksum}!={check_num}")
					try:
						f_data = Books.dep_book(instId)
						return books_handle(instId, [f_data], "全量查询")
					except Exception:
						# logging.exception("强刷深度数据失败")
						return
				else:
					# logging.debug("过滤异常数据")
					return
			else:
				logging.debug(f"成功合并深度数据\t{instId}")
				update(ts, all_asks, all_bids)
		else:
			logging.debug(f"全量深度数据\t{instId}")
			update(ts, incr_asks, incr_bids)
	books = Books.books_data[instId]
	is_swap = instId.endswith("-SWAP")
	item = dict()
	item_unix_ts = int(Books.tss[instId])
	local_ts_key = 'book_' + instId
	if local_ts_key in local_ts_cache and local_ts_cache[local_ts_key][0] >= item_unix_ts:
		logging.error([local_ts_key, source_type,
		               "时间顺序错误，忽略这条数据\nlocal={}\nremote={}".format(local_ts_cache[local_ts_key], (item_unix_ts, data))])
		return
	local_unix_ts = HeaderUtils.get_unix_timestamp_ns()
	item['timestamp'] = item_unix_ts
	item['exchange'] = 'okex'
	item['asset_type'] = 'swap' if is_swap else 'spot'
	item['symbol'] = instId
	item['local_timestamp'] = local_unix_ts
	asks, bids = books['asks'], books['bids']
	for i in range(20):
		ask, bid = asks[i], bids[i]
		item[f'ask_{i}_p'] = float(ask[0])
		item[f'bid_{i}_p'] = float(bid[0])
		assert i == 0 or item[f'ask_{i}_p'] > item[f'ask_{i - 1}_p']
		assert i == 0 or item[f'bid_{i}_p'] < item[f'bid_{i - 1}_p']
		if is_swap:
			ctVal = Instruments.ctVal("SWAP", instId)
			item[f'ask_{i}_v'] = float(ask[1]) * ctVal
			item[f'bid_{i}_v'] = float(bid[1]) * ctVal
		else:
			item[f'ask_{i}_v'] = float(ask[1])
			item[f'bid_{i}_v'] = float(bid[1])
	item['time'] = HeaderUtils.get_timestamp(item_unix_ts, False)
	item['local_time'] = HeaderUtils.get_timestamp(local_unix_ts, False)
	local_ts_cache[local_ts_key] = (item_unix_ts, data)
	item['bookId'] = ts
	item['id'] = item['bookId']
	if instId == Currency.BTCUSDT and (not mkt.spot_tick_line or not_dup_check(mkt.spot_tick_line[-1], item)):
		line_append(mkt.spot_tick_line, item)
	elif instId == Currency.BTCUSDT_SWAP and (not mkt.swap_tick_line or not_dup_check(mkt.swap_tick_line[-1], item)):
		line_append(mkt.swap_tick_line, item)


def not_dup_check(line0, last_0):
	last = {**last_0}
	del last['timestamp']
	del last['local_timestamp']
	del last['id']
	del last['bookId']
	del last['local_time']
	del last['time']
	line = {**line0}
	del line['timestamp']
	del line['local_timestamp']
	del line['id']
	del line['bookId']
	del line['local_time']
	del line['time']
	return not operator.eq(line, last)


def line_append(lines: list, item, sort_key="id"):
	if len(lines) > 0:
		if item['timestamp'] > lines[-1]['timestamp']:
			lines.append(item)
		elif sort_key in item:
			iid = item[sort_key]
			lid = lines[-1][sort_key]
			if iid > lid:
				lines.append(item)
			elif iid == lid:
				pass
			else:
				raise Exception()
		else:
			raise Exception()
	else:
		lines.append(item)
