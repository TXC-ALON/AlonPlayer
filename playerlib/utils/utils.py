from numpy import NaN
import time
import multiprocessing
import inspect

"""
功能：
参数：
返回值：
"""


def print_dict(default_dict):
    """
    功能：给定字典，打印里面的键值对
    参数：- Dict，
    返回值：无 仅打印输出
    """
    for key, value in default_dict.items():
        print(key + ": " + str(value))


def print_video_list_simple(video_dict, order=None):
    """
    功能：给定一个字典，以简单方式输出video_dict的内容
    参数：- Dict，order
    返回值：无 仅打印输出
    """
    if order is None:
        for video in video_dict:
            video.print_video_simple()
    else:
        for order, video in enumerate(video_dict, start=1):
            video.print_video_simple(order)


def print_sorted_dict(video_dict):
    """
    功能：给定字典，对字典的键进行排序
    参数：- Dict
    返回值：无 仅排序
    """
    sorted_keys = sorted(video_dict.keys())  # 对字典的键进行排序
    for key in sorted_keys:
        value = video_dict[key]
        print(key + ": " + str(value))


def convert_case(my_list):
    """
    功能：给定一个list，将list的全部统一大小写，并都加入list内
    参数：- list
    返回值：带有大小写的list
    """
    upper_list = [item.upper() for item in my_list]
    lower_list = [item.lower() for item in my_list]
    return upper_list + lower_list


def parse_size_string(size_string):
    """
    功能：给定一个带有字节大小的字符串，将其进行识别,支持浮点数
    参数：- str  eg：1MB,5.6gb
    返回值：返回字节数
    """
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


def format_time(seconds):
    """
    功能：给定一个时间，对其格式化,按照天，小时，分钟，秒，毫秒来分配
    参数：- str(要能转为数字)、num
    返回值：str
    """
    if seconds == NaN:
        return "DURATION ERROR"
    try:
        seconds = float(seconds)
    except:
        print("INPUT FORMAT ERROR")
    seconds, milliseconds = divmod(seconds, 1)
    milliseconds *= 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours >= 24:
        days, hours = divmod(hours, 24)
        return "{:d}days {:02d}:{:02d}:{:02d}".format(int(days), int(hours), int(minutes), int(seconds))
    elif hours > 0:
        return "{:02d}:{:02d}:{:02d}:".format(int(hours), int(minutes), int(seconds))
    else:
        return "{:02d}:{:02d}".format(int(minutes), int(seconds))


def timer_decorator(func):
    """
    功能：函数包裹器，打印函数运行时间
    参数：- fun
    返回值：wrapper
    """

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 记录开始时间

        result = func(*args, **kwargs)  # 执行被装饰的函数

        end_time = time.perf_counter()  # 记录结束时间
        execution_time = end_time - start_time  # 计算执行时间

        print(f"函数 {func.__name__} 的执行时间为: {execution_time} 秒")

        return result

    return wrapper


def get_max_threads():
    """
    功能：获得当前机器的最大线程数
    参数：无
    返回值：thread_num
    """
    max_threads = multiprocessing.cpu_count()
    return max_threads


def get_function_info(if_print=False):
    """
    功能：获得当前文件下函数信息
    参数：无
    返回值：list
    """
    frame = inspect.currentframe().f_back
    functions = [(name, obj, inspect.getdoc(obj)) for name, obj in frame.f_globals.items() if inspect.isfunction(obj)]
    function_count = len(functions)
    if if_print:
        print(f"当前文件自定义了 {function_count} 个函数：")
        print("--------------------------------")
        for order, (name, _, docstring) in enumerate(functions, start=1):
            print(f"{order} 函数名：{name}")
            print(f"注释：\n{docstring}")
            print("--------------------------------")
    return functions


if __name__ == '__main__':
    function_info = get_function_info(1)
