f"""
OKEX 用户检验/加解密工具
"""
import base64
import datetime
import hmac
import json
from hmac import HMAC

import time
import zlib

apikey = "03af8586271056d2ed61276ec8a96be111a367bec48891a45a4ba3fce280549f"
secretkey = "d90e4114442e1fd107c1f240eef44bbf7ac0ce2eb0ce54078e270566145e3f54"
passPhrase = ""

# override_api_baseurl = "https://testnet.binancefuture.com"
override_api_baseurl = "https://fapi.binance.com"


def crc32(str):
	return zlib.crc32(str.encode('utf-8'))


def signature(timestamp, method, request_path, body, secret_key):
	if str(body) == '{}' or str(body) == 'None':
		body = ''
	message = str(timestamp) + str.upper(method) + request_path + str(body)
	mac = hmac.new(bytes(secret_key, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod='sha256')
	d = mac.digest()
	return base64.b64encode(d)


class HeaderUtils:
	method = "GET"
	body = ""

	def __init__(self):
		pass

	@staticmethod
	def get_timestamp(ts_ns=None, ms_len3=True):
		now = datetime.datetime.utcfromtimestamp(ts_ns / 1000.0 if ts_ns else time.time())
		if ms_len3:
			t = now.isoformat("T", "milliseconds")
		else:
			t = now.isoformat("T")
		return t + "Z"

	@staticmethod
	def get_unix_timestamp():
		return round(time.time())

	@staticmethod
	def get_unix_timestamp_ns():
		return round(time.time() * 1000)

	@staticmethod
	def pre_hash(timestamp, method, request_path, body):
		return str(timestamp) + str.upper(method) + request_path + body

	@staticmethod
	def sign_encode(message, secretKey):
		mac: HMAC = hmac.new(
			bytes(secretKey, encoding="utf8"),
			bytes(message, encoding="utf-8"),
			digestmod="sha256",
		)
		d = mac.digest()
		return base64.b64encode(d)

	def get_rest_header(self, request_path, method="GET", params: dict = None):
		timestamp = self.get_timestamp()
		sign = signature(timestamp, method, request_path, json.dumps(params) if params else "", secretkey)
		header = dict()
		header["Content-Type"] = "application/json"
		header["OK-ACCESS-KEY"] = apikey
		header["OK-ACCESS-SIGN"] = sign.decode("utf-8")
		header["OK-ACCESS-TIMESTAMP"] = timestamp
		header["OK-ACCESS-PASSPHRASE"] = passPhrase
		return header


HEADER = HeaderUtils()


def gen_send_msg(op: str, *args: dict) -> str:
	return f'{{"op": "{op}", "args": [{",".join([json.dumps(arg) for arg in args])}]}}'


def gen_send_order_msg(order_id, op: str, *args: dict) -> str:
	if isinstance(order_id, int):
		order_id = str(order_id)
	return f'{{"id": {order_id}, "op": "{op}", "args": [{",".join([json.dumps(arg) for arg in args])}]}}'


# 处理推送信息
def get_resp_data(resp: dict):
	return resp.get("data")


def parse_channel_resp(resp: dict):
	"""

	:rtype: channel,instId,datas
	"""
	return resp.get("arg").get("channel"), resp.get("arg").get("instId"), resp.get("data")


if __name__ == '__main__':
	print(HeaderUtils.get_timestamp(HeaderUtils.get_unix_timestamp_ns()))
	print(HeaderUtils.get_timestamp(HeaderUtils.get_unix_timestamp_ns(), False))
	print(HeaderUtils.get_unix_timestamp())
	print(HeaderUtils.get_unix_timestamp_ns())
