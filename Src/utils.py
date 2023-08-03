def printDict(Dict):
    for key, value in Dict.items():
        print(key + ": " + str(value))

def printSortedDict(Dict):
    sorted_keys = sorted(Dict.keys())  # 对字典的键进行排序
    for key in sorted_keys:
        value = Dict[key]
        print(key + ": " + str(value))

def convert_case(my_list):
    upper_list = [item.upper() for item in my_list]
    lower_list = [item.lower() for item in my_list]
    return upper_list + lower_list


def parse_size_string(size_string):
    size_string = size_string.strip().lower()
    units = {'b': 1, 'kb': 1024, 'mb': 1024 ** 2, 'gb': 1024 ** 3, 'tb': 1024 ** 4}

    for unit, multiplier in units.items():
        if size_string.endswith(unit):
            try:
                size = float(size_string[:-len(unit)].strip())
                return int(size * multiplier)
            except ValueError:
                pass

    try:
        return int(float(size_string))
    except ValueError:
        raise ValueError("Invalid size string format.")