f"""
行情深度数据
"""
import logging
import zlib

import OkexRest

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


def update_book(bs_u, bs_f, is_bid=False):
	change_count = 0
	delete_count = 0
	# 遍历增量
	for i in bs_u:
		u_price = i[0]
		u_pap_num = float(i[1])
		insert_flag = True
		for j in bs_f:
			f_price = i[0]
			f_pap_num = float(i[1])
			# 增量更新全量
			if u_price == f_price:
				insert_flag = False
				if u_pap_num <= 0:
					# 删除
					bs_f.remove(j)
					change_count += 1
					delete_count += 1
					break
				else:
					# 替换
					j[1] = i[1]
					j[2] = i[2]
					j[3] = i[3]
					if u_pap_num != f_pap_num: change_count += 1
					break
		# 增量插入全量
		if insert_flag and u_pap_num > 0:
			bs_f.append(i)
			change_count += 1
	bs_f.sort(key=lambda price:sort_num(price[0]), reverse=is_bid)
	return bs_f, change_count


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


if __name__ == '__main__':
	all_bids = [['61982.6', '781', '0', '22'], ['61979.2', '32', '0', '2'], ['61976.5', '133', '0', '8'],
	            ['61973.4', '42', '0', '2'], ['61973.3', '2', '0', '1'], ['61972.2', '21', '0', '1'],
	            ['61971.7', '90', '0', '1'], ['61970.4', '2', '0', '1'], ['61970.3', '7', '0', '1'],
	            ['61970.2', '85', '0', '4'], ['61969.1', '17', '0', '1'], ['61968.3', '39', '0', '2'],
	            ['61967.3', '257', '0', '1'], ['61967.1', '8', '0', '1'], ['61967', '5', '0', '2'],
	            ['61966.7', '2', '0', '1'], ['61966.2', '1', '0', '1'], ['61965.5', '2', '0', '1'],
	            ['61964.8', '17', '0', '1'], ['61964.6', '57', '0', '1'], ['61964.4', '3', '0', '1'],
	            ['61964.2', '15', '0', '1'], ['61964.1', '3', '0', '1'], ['61964', '21', '0', '1'],
	            ['61963.9', '50', '0', '1'], ['61962.7', '10', '0', '1'], ['61962.6', '55', '0', '1'],
	            ['61955.1', '24', '0', '1']]

	incr_bids = [['61963.9', '0', '0', '0'], ['61954.7', '8', '0', '1'], ['61948.1', '4', '0', '1']]

	merge_data(all_bids, incr_bids, False)
	print(all_bids)

	all_bids = [['61982.6', '781', '0', '22'], ['61979.2', '32', '0', '2'], ['61976.5', '133', '0', '8'],
	            ['61973.4', '42', '0', '2'], ['61973.3', '2', '0', '1'], ['61972.2', '21', '0', '1'],
	            ['61971.7', '90', '0', '1'], ['61970.4', '2', '0', '1'], ['61970.3', '7', '0', '1'],
	            ['61970.2', '85', '0', '4'], ['61969.1', '17', '0', '1'], ['61968.3', '39', '0', '2'],
	            ['61967.3', '257', '0', '1'], ['61967.1', '8', '0', '1'], ['61967', '5', '0', '2'],
	            ['61966.7', '2', '0', '1'], ['61966.2', '1', '0', '1'], ['61965.5', '2', '0', '1'],
	            ['61964.8', '17', '0', '1'], ['61964.6', '57', '0', '1'], ['61964.4', '3', '0', '1'],
	            ['61964.2', '15', '0', '1'], ['61964.1', '3', '0', '1'], ['61964', '21', '0', '1'],
	            ['61962.7', '10', '0', '1'], ['61962.6', '55', '0', '1'], ['61955.1', '24', '0', '1'],
	            ['61954.7', '8', '0', '1'], ['61948.1', '4', '0', '1']]
