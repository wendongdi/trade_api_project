f"""
字典工具
"""
import re

ColumnMap = dict()

with open("ws_dictionary.txt", "r", encoding="utf-8") as dtxt:
    for line in dtxt.readlines():
        if re.compile("[a-zA-Z>]").match(line):
            line = line.strip().replace("> ", "")
            args = line.split("\t")
            if len(args) > 1:
                ColumnMap[args[0]] = args[-1].split("，")[0]


def data_analysis(title, instId, data):
    for k, v in data.items():
        colname = ColumnMap[k] if k in ColumnMap else "unknownColumn"
        print(title, instId, k, colname, v)


