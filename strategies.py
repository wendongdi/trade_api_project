from ws4py.client.threadedclient import WebSocketClient

import constants
import handlers
import utils
from constants import Operation, Channel
from handlers import *

f"""
配合{handlers}自定义逻辑
"""

HTTP_URL: str = "https://www.okex.com"
WS_PRIVATE_URL: str = "wss://ws.okex.com:8443/ws/v5/private"
WS_PUBLIC_URL: str = "wss://ws.okex.com:8443/ws/v5/public"

EventHandlers = {
	Operation.SUBSCRIBE:subscribe_handle,
	Operation.ERROR:err_handle
}

ChannelHandlers = {
	Channel.INSTRUMENTS:instruments_handle,
	Channel.TICKERS:tick_handle_proxy,
	Channel.TRADES:trade_handle_proxy,
	Channel.BOOKS50:books_handle_proxy,
	Channel.BOOKS:books_handle_proxy,
}


class WsStrategy(object):
	URL: str = None
	agent: WebSocketClient = None

	def __init__(self, URL: str):
		self.URL = URL

	def set_websocket(self, ws: WebSocketClient):
		self.agent = ws

	def open_login(self):
		# todo 登录
		raise NotImplementedError

	def open_subscribe(self):
		# todo 订阅
		raise NotImplementedError

	def ws_opened(self):
		"""
		# 果需要订阅多条数据，可以在下面使用ws.send方法来订阅
		# 其中 op 的取值为 1--subscribe 订阅； 2-- unsubscribe 取消订阅 ；3--login 登录
		# args: 取值为频道名，可以定义一个或者多个频道
		@return:
		"""
		logging.debug("连接成功～")
		self.open_login()
		self.open_subscribe()

	def ws_closed(self, code, reason):
		logging.debug(f"连接中断～\t{code}\t{reason}")

	def msg_handle(self, json_msg):
		if 'event' in json_msg:
			event = json_msg['event']
			handler = common_handle if event not in EventHandlers else EventHandlers[event]
			handler(json_msg)
		else:
			channel, instId, datas = utils.parse_channel_resp(json_msg)
			handler = data_common_handle if channel not in ChannelHandlers else ChannelHandlers[channel]
			handler(instId, datas)


class WsPublicStrategy(WsStrategy):
	mkt = None

	def __init__(self, URL: str = WS_PUBLIC_URL):
		super().__init__(URL)

	def open_login(self):
		pass

	def open_subscribe(self):
		channels = [
			{"channel":Channel.INSTRUMENTS, "instType":"SWAP"},
		]
		for instId in constants.INST_IDS:
			Books.init(instId)
			channels.append({"channel":Channel.BOOKS, "instId":instId})
			# channels.append({"channel": Channel.TICKERS, "instId": instId})
			channels.append({"channel":Channel.TRADES, "instId":instId})

		self.agent.send(utils.gen_send_msg("subscribe", *channels))
