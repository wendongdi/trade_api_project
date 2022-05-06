f"""
行情深度数据
"""
import json
import logging

import time
import zlib

import OkexRest

fd = None

f"""
 asks和bids值数组举例说明：
 ["411.8", "10", "1", "4"]
    411.8为深度价格，
    10为此价格的合约张数，
    1为此价格的强平单个数，
    4为此价格的订单个数
"""
# 深度数据，instId做key
# ask升序，bid降序
books_data = dict()
tss = dict()


def init(instId):
	books_data[instId] = {
		'asks':[], 'bids':[]
	}
	tss[instId] = 0


def force_update(instId):
	logging.warning(f"强刷全量深度数据\t{instId}")
	data = dep_book(instId)
	ts = int(data['ts'])
	tss[instId] = ts
	books_data[instId]['asks'] = data['asks']
	books_data[instId]['bids'] = data['bids']


def dep_book(instId, depth=400):
	"""
	asks和bids值数组举例说明：
		["411.8", "10", "1", "4"]
		411.8为深度价格，
		10为此价格的合约张数，
		1为此价格的强平单个数，
		4为此价格的订单个数
	:param instId: 产品ID
	:param depth: 深度
	:return:
	"""
	return OkexRest.books(instId, depth)['data'][0]


def merge_data(all: list, apd: list, asc_sort=True):
	"""
	合并深度数据
	:param all: 全量数据，ask升序，bid降序
	:param apd: 增量数据，ask升序，bid降序
	:param asc_sort: ask升序，bid降序，默认升序
	"""

	def comp(xa, xb):
		if asc_sort:
			return xa < xb
		else:
			return xa > xb

	alli = 0
	apdi = 0

	while apdi < len(apd) and alli < len(all):
		apd_item = apd[apdi]
		all_item = all[alli]
		if comp(apd_item[0], all_item[0]):
			if float(apd_item[1]) > 0:
				all.insert(alli, apd_item)
			apdi += 1
		elif apd_item[0] == all_item[0]:
			if float(apd_item[1]) > 0:
				all[alli] = apd_item
				alli += 1
			else:
				all.pop(alli)
			apdi += 1
		else:
			alli += 1

	if apdi < len(apd):
		for item in apd[apdi:]:
			if float(item[1]) > 0:
				all.append(item)

	logging.debug(f"合并\t{all}")


def sort_num(n):
	if n.isdigit():
		return int(n)
	else:
		return float(n)


def update_bids(bids_u, bids_p):
	# bids合并
	for i in bids_u:
		bid_price = i[0]
		for j in bids_p:
			if bid_price == j[0]:
				if float(i[1]) <= 0:
					bids_p.remove(j)
					break
				else:
					del j[1]
					j.insert(1, i[1])
					break
		else:
			if float(i[1]) > 0:
				bids_p.append(i)
	else:
		bids_p.sort(key=lambda price:sort_num(price[0]), reverse=True)
	return bids_p


def update_asks(asks_u, asks_p):
	# asks合并
	for i in asks_u:
		ask_price = i[0]
		for j in asks_p:
			if ask_price == j[0]:
				if float(i[1]) <= 0:
					asks_p.remove(j)
					break
				else:
					del j[1]
					j.insert(1, i[1])
					break
		else:
			if float(i[1]) > 0:
				asks_p.append(i)
	else:
		asks_p.sort(key=lambda price:sort_num(price[0]))
	return asks_p


def check(bids, asks):
	# 获取bid档str
	bids_l = []
	bid_l = []
	count_bid = 1
	while count_bid <= 25:
		if count_bid > len(bids):
			break
		bids_l.append(bids[count_bid - 1])
		count_bid += 1
	for j in bids_l:
		str_bid = ':'.join(j[0: 2])
		bid_l.append(str_bid)
	# 获取ask档str
	asks_l = []
	ask_l = []
	count_ask = 1
	while count_ask <= 25:
		if count_ask > len(asks):
			break
		asks_l.append(asks[count_ask - 1])
		count_ask += 1
	for k in asks_l:
		str_ask = ':'.join(k[0: 2])
		ask_l.append(str_ask)
	# 拼接str
	num = ''
	if len(bid_l) == len(ask_l):
		for m in range(len(bid_l)):
			num += bid_l[m] + ':' + ask_l[m] + ':'
	elif len(bid_l) > len(ask_l):
		# bid档比ask档多
		for n in range(len(ask_l)):
			num += bid_l[n] + ':' + ask_l[n] + ':'
		for l in range(len(ask_l), len(bid_l)):
			num += bid_l[l] + ':'
	elif len(bid_l) < len(ask_l):
		# ask档比bid档多
		for n in range(len(bid_l)):
			num += bid_l[n] + ':' + ask_l[n] + ':'
		for l in range(len(bid_l), len(ask_l)):
			num += ask_l[l] + ':'

	new_num = num[:-1]
	int_checksum = zlib.crc32(new_num.encode())
	fina = change(int_checksum)
	return fina


def change(num_old):
	num = pow(2, 31) - 1
	if num_old > num:
		out = num_old - num * 2 - 2
	else:
		out = num_old
	return out


lock_file = '/tmp/okex-books-lock'


# 服务器唯一的book数据下载器
def book_downloader(instIds):
	global fd
	if fd is None:
		import fcntl
		# 服务器文件锁
		fd = open(lock_file, 'a+')
		try:
			fcntl.flock(fd, fcntl.LOCK_EX)
			while True:
				for instId in instIds:
					data = dep_book(instId)
					wf = open(lock_file + instId, "w+")
					wf.write(json.dumps(data))
					wf.close()
					time.sleep(0.10)
		finally:
			try:
				fcntl.flock(fd, fcntl.LOCK_UN)
			except:
				pass
			try:
				fd.close()
			except:
				pass
			try:
				fd = None
			except:
				pass
