def printDict(Dict):
    for key, value in Dict.items():
        print(key + ": " + str(value))

def printSortedDict(Dict):
    sorted_keys = sorted(Dict.keys())  # 对字典的键进行排序
    for key in sorted_keys:
        value = Dict[key]
        print(key + ": " + str(value))