from numpy import NaN
import time
import multiprocessing


def print_dict(video_dict):
    for key, value in video_dict.items():
        print(key + ": " + str(value))


def print_video_list_simple(video_dict, order=None):
    i = 1
    for video in video_dict:
        video.print_video_simple(i)
        i += 1


def print_sorted_dict(video_dict):
    sorted_keys = sorted(video_dict.keys())  # 对字典的键进行排序
    for key in sorted_keys:
        value = video_dict[key]
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


def format_time(seconds):
    if seconds == NaN:
        return "DURATION ERROR"
    seconds = float(seconds)
    seconds, milliseconds = divmod(seconds, 1)
    milliseconds *= 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if int(hours) != 0:
        return "{:02d}h:{:02d}m:{:02d}s:{:03dms}".format(int(hours), int(minutes), int(seconds), int(milliseconds))
    else:
        return "{:02d}m{:02d}s".format(int(minutes), int(seconds))


def compare_video(video):
    return (video.file_size_pure, video.file_name, video.duration)


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 记录开始时间

        result = func(*args, **kwargs)  # 执行被装饰的函数

        end_time = time.perf_counter()  # 记录结束时间
        execution_time = end_time - start_time  # 计算执行时间

        print(f"函数 {func.__name__} 的执行时间为: {execution_time} 秒")

        return result

    return wrapper


def get_max_threads():
    max_threads = multiprocessing.cpu_count()
    return max_threads
