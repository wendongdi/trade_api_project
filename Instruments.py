f"""
产品的合约面值
"""
from typing import Dict

import OkexRest
import constants

CtVals: Dict[str, float] = dict()


def ctVal(instType: str, instId: str) -> float:
	if instId in CtVals:
		return CtVals[instId]
	else:
		instId_ctVal = float(OkexRest.instruments(instType, instId)['data'][0]['ctVal'])
		CtVals[instId] = instId_ctVal
		return instId_ctVal


if __name__ == '__main__':
	print(ctVal("SWAP", constants.Currency.BTCUSDT_SWAP))
