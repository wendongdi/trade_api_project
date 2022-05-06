f"""
OKEX 实时接口工具
"""
import logging

import requests
import urllib3

import strategies
import utils

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request_get(request_path, params: dict = None):
	# http时需要访问什么接口，headers和url都得设置成相同的
	if params:
		params_url = "&".join([k + "=" + v for k, v in params.items()])
		request_path = request_path + "?" + params_url
	target_url = strategies.HTTP_URL + request_path
	headers = utils.HEADER.get_rest_header(request_path=request_path)
	response = requests.get(target_url, headers=headers, verify=False)
	json = response.json()
	if json['code'] != "0":
		logging.debug(f"Rest接口调用异常：req:{target_url}\tresp:{json}\theaders:{headers}")
		pass
	return json


def request_post(request_path, params: dict = None):
	target_url = strategies.HTTP_URL + request_path
	headers = utils.HEADER.get_rest_header(request_path=request_path, method="POST", params=params)
	response = requests.post(target_url, json=params, headers=headers, verify=False)
	json = response.json()
	if json['code'] != "0":
		# logging.error(f"Rest接口调用异常：req:{target_url}\tresp:{json}\theaders:{headers}")
		pass
	return json


def instruments(instType, instId=None, uly=None):
	params: dict = {"instType":instType}
	if instId:
		params["instId"] = instId
	if uly:
		params["uly"] = uly
	return request_get("/api/v5/public/instruments", params)


def books(instId, sz=20):
	return request_get("/api/v5/market/books", {"instId":instId, "sz":str(sz)})
