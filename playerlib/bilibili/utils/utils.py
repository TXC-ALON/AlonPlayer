import json
import re
from datetime import datetime

from playerlib import format_time


def bvid2aid(bvid: str) -> int:
    """
    BV 号转 AV 号。

    Args:
        bvid (str):  BV 号。

    Returns:
        int: AV 号。
    """
    table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def dec(x):
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return (r - add) ^ xor

    return dec(bvid)


def print_bili_video_dict_simple(video_dict, order=None):
    """
    功能：给定一个字典，以简单方式输出video_dict的内容
    参数：- Dict，order
    返回值：无 仅打印输出
    """
    if order is None:
        for video in video_dict:
            print_video_simple(video)
    else:
        for order, video in enumerate(video_dict, start=1):
            print_video_simple(video, order)


def print_video_simple(videoinfo, order=None):
    if order is None:
        print("bvid[{0}],时长=[{1}],大小=[{2}] resolution=[{3}*{4}]"
              .format(videoinfo.file_name, videoinfo.timeout, videoinfo.file_size, videoinfo.width, videoinfo.height))
    else:
        print("{5}:名称[{0}],时长=[{1}],大小=[{2}] resolution=[{3}*{4}]"
              .format(videoinfo.file_name, videoinfo.timeout, videoinfo.file_size, videoinfo.width, videoinfo.height,
                      order))


def convert_pubdate(pubdate):
    current_time = datetime.now()
    timestamp = int(pubdate)
    pubdate_time = datetime.fromtimestamp(timestamp)
    return pubdate_time.strftime("%Y-%m-%d %H:%M:%S")


def print_owner_info(_owner):
    owner = _owner
    if owner is not None:
        print("UP : {0} mid {1}".format(owner['name'], owner['mid']))


def print_video_stat(_video_stat):
    stat = _video_stat
    if stat is not None:
        print("视频[{7}] : 播放量 {0} 弹幕量 {1} 评论数 {2} 点赞{3} 投币{4} 收藏{5} 分享{6} "
              .format(stat['view'], stat['danmaku'], stat['reply'], stat['like'],
                      stat['coin'], stat['favorite'], stat['share'], stat['aid']))


def calculate_length(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')  # 中文字符的正则表达式模式
    chinese_count = len(re.findall(pattern, text))  # 统计中文字符数量
    total_length = len(text) + chinese_count  # 计算总长度
    return total_length


import wcwidth


def format_string(video_time, marker, text):
    marker_width = wcwidth.wcswidth(marker)  # marker的显示宽度
    text_width = wcwidth.wcswidth(text)  # text的显示宽度
    fill_spaces = max(10, 20 + marker_width - text_width)  # 需要填充的空格数量
    formatted_text = "{0}:  {1}{2}{3}".format(video_time, text, " " * fill_spaces, marker)
    return formatted_text


def print_single_damu(damu):
    send_time = convert_pubdate(damu.send_time)
    video_time = format_time(damu.dm_time)
    text = damu.text
    output = format_string(video_time, send_time, text)
    print(output)


# todo 格式化字符串输出？
def write_json(list, filename):
    json_data = json.dumps(list)
    with open(filename, 'w') as file:
        file.write(json_data)
