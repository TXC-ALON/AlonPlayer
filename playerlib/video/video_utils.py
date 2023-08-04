from playerlib.video.video_class import *
from playerlib.video.video_searcher import *
from playerlib.utils.utils import *
from playerlib.constants import *

import os
import shutil

"""
功能：
参数：
返回值：
"""


def move_video_to_folder(video_path_list: list, _to_folder: str):
    """
    功能：将列表里的文件移到另一个文件夹
    参数：list(里面是video的 path，不用强调是绝对路径）,str 目标文件夹
    返回值：print
    """
    to_folder = os.path.abspath(_to_folder)
    if len(video_path_list) == 0:
        print("video_path_list [{}] is empty!!!".format(video_path_list))
    else:
        print("this time move {} files".format(len(video_path_list)))
        for order, video_path in enumerate(video_path_list, start=1):
            filename = os.path.basename(video_path)  # 获取文件名
            from_folder = os.path.dirname(video_path)
            destination = os.path.join(to_folder, filename)  # 目标文件夹中的路径
            print("{3}-- move {0} from {1} to {2}".format(filename, from_folder, to_folder, order))
            try:
                shutil.move(video_path, destination)  # 移动文件到目标文件夹
            except FileNotFoundError:
                print("FileNotFoundError: The file '{0}' does not exist.".format(video_path))
            except shutil.Error as e:
                print("shutil.Error: Failed to move the file '{0}'. Error: {1}".format(video_path, str(e)))


def move_video_from_here_to_there(_from_folder: str, _to_folder: str):
    """
    功能：将一个文件夹下的所有视频文件移动到另一个文件夹
    参数：str，str
    返回值：none
    """
    from_folder = os.path.abspath(_from_folder)
    to_folder = os.path.abspath(_to_folder)
    vs = VideoSearcher(from_folder)
    video_list = vs.get_video_path()
    if len(video_list) == 0:
        print("from_folder [{}] is empty!!!".format(from_folder))
    else:
        move_video_to_folder(video_list, to_folder)


def swap_path(folder1, folder2):
    """
    功能：简单交换一下源文件夹和目标文件夹
    参数：str，str
    返回值：tuple
    """
    temp = folder1
    folder1 = folder2
    folder2 = temp
    return folder1, folder2


if __name__ == '__main__':
    src = r"E:\00Learning\AlonPlayer\test\testfile\testmove\src"
    dst = r"E:\00Learning\AlonPlayer\test\testfile\testmove\dst"
    # src, dst = swap_path(src, dst)
    move_video_from_here_to_there(src, dst)
