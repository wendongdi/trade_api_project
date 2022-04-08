f"""
账号信息
"""
import OkexRest


# 账户余额
def balance(ccy=None):
    params = {"ccy": ccy} if ccy else {}
    return OkexRest.request_get("/api/v5/account/balance", params)['data']


# 账户配置
def config():
    return OkexRest.request_get("/api/v5/account/config")['data']


# 账户最大可转余额
def max_withdrawal(ccy=None):
    params = {"ccy": ccy} if ccy else {}
    return OkexRest.request_get("/api/v5/account/max-withdrawal", params)['data']


if __name__ == '__main__':
    print(balance("BTC"))






