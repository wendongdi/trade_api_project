f"""
OKEX websocket工具
"""
import json
import logging
import threading
import time

from ws4py.client.threadedclient import WebSocketClient

from strategies import WsStrategy, WsPublicStrategy


class OKExRunner(WebSocketClient):
	"""
	提供websocket环境
	"""
	strategy: WsStrategy = None

	def __init__(
			self,
			ws_strategy: WsStrategy,
			stop_hook,
			protocols=None,
			extensions=None,
			heartbeat_freq=None,
			ssl_options=None,
			headers=None,
			exclude_headers=None,
	):
		super().__init__(
			ws_strategy.URL,
			protocols,
			extensions,
			heartbeat_freq,
			ssl_options,
			headers,
			exclude_headers,
		)
		ws_strategy.set_websocket(self)
		self.stop_hook = stop_hook
		self.strategy = ws_strategy
		self.to_reroot = False

	def send(self, payload, binary=False):
		try:
			return super().send(payload, binary)
		except Exception:
			logging.exception("websocket链接异常")

	def run_forever(self):
		threading.Thread(
			target=self.send_heart_beat, args=(), daemon=True, name="heart_beat"
		).start()  # 新建一个线程来发送心跳包
		super().run_forever()

	def ponged(self, pong):
		logging.debug(f"pong received.\t{pong}")

	def opened(self):
		self.strategy.ws_opened()

	def closed(self, code, reason=None):
		self.strategy.ws_closed(code, reason)
		self.to_reroot = True

	def unhandled_error(self, error):
		logging.error(f"Failed to receive data\t{error}")

	def close_connection(self):
		super().close_connection()

	def received_message(self, resp):
		if str(resp) == "pong":
			self.ponged(resp)
			return
		try:
			json_msg = json.loads(str(resp))
		except Exception as e:
			logging.info(f"非JSON响应消息：\t{resp}")
			raise e
		self.strategy.msg_handle(json_msg)

	def send_heart_beat(self):
		ping = 'ping' or '{"event":"ping"}'
		while not self.to_reroot:
			if self.stop_hook():
				self.close(reason='stop hook')
				continue
			time.sleep(5)  # 每隔5秒交易所服务器发送心跳信息
			sent = False
			while sent is False:  # 如果发送心跳包时出现错误，则再次发送直到发送成功为止
				self.send(ping)
				sent = True
				logging.debug("Ping sent.")


def default_stop_hook():
	return False


def run_ws_public(a_sync=False, stop_hook=default_stop_hook):
	pc_ws = None
	try:
		def run_forever():
			while True:
				pc_ws = OKExRunner(WsPublicStrategy(), stop_hook)
				pc_ws.connect()

				pc_ws.run_forever()
				print("pc_wd reboot...")
				pc_ws.close_connection()
				pc_ws.close()
				time.sleep(5)

		if a_sync:
			thread = threading.Thread(
				target=run_forever, args=(), daemon=True, name="run_forever"
			)
			thread.start()
			return thread
		else:
			run_forever()
			return None
	except Exception:
		logging.exception("OKExRunner error")
		pc_ws.close()
