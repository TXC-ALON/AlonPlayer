import os
from playerlib.constants import *
from playerlib.utils.utils import *
from playerlib.video.Video import *
import time
import threading


class VideoSearcher:
    def __init__(self, path, search_video_type=None, min_file_limit="0Mb"):
        if search_video_type is None:
            search_video_type = DEFAULT_VIDEO_FORMAT_LIST
        self.path = path
        self.absolute_path = os.path.abspath(path)
        self.search_type = convert_case(search_video_type)
        self.min_file_limit = parse_size_string(min_file_limit)
        self.searched_video_path = []
        self.searched_video_path = self.get_video_path()
        self.searched_video = []
        # self.searched_video = self.get_video()
        self.searched_video = self.get_video_multithread(MULTITHREAD)

    # @timer_decorator
    def get_video_path(self):
        video_files = []
        trash_video_files = []
        folder_path = self.absolute_path
        extensions = self.search_type
        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if file_size > self.min_file_limit:  # 1MB in bytes
                        video_files.append(file_path)
                    else:
                        trash_video_files.append(file_path)

        return video_files

    @timer_decorator
    def get_video(self):
        video_list = []
        for video_path in self.searched_video_path:
            temp_video = Video(video_path)
            video_list.append(temp_video)
        return video_list

    @timer_decorator
    def get_video_multithread(self, num_threads=2):
        video_list = []
        threads = []

        def process_video(video_path):
            temp_video = Video(video_path)
            video_list.append(temp_video)

        # 创建线程并启动
        for video_path in self.searched_video_path:
            t = threading.Thread(target=process_video, args=(video_path,))
            threads.append(t)
            t.start()

        # 等待所有线程完成
        for t in threads:
            t.join()

        return video_list

    def print_searched_video(self):
        for video in self.searched_video:
            video.print_video()

    def print_searched_video_simple(self):
        order = 1
        for video in self.searched_video:
            video.print_video_simple(order)
            order += 1

    def sort_videos_by_name(self, is_reverse=False):
        sorted_video = sorted(self.searched_video, key=lambda v: (v.file_name, float(v.duration)))
        if is_reverse is True:
            sorted_video.reverse()
        return sorted_video

    def sort_videos_by_duration(self, decrease=False):
        sorted_video = sorted(self.searched_video, key=lambda v: (float(v.duration), v.file_name))
        if decrease is True:
            sorted_video.reverse()
        return sorted_video


if __name__ == '__main__':
    get_function_info(1)
    start_time = time.time()
    VS = VideoSearcher(r"E:\00Learning\AlonPlayer", min_file_limit="0.01MB")
    # 计算步骤1的耗时
    step1_time = time.time() - start_time
    print("步骤1耗时：", step1_time, "秒")
    # print(VS.searched_video_path)
    # sorted_videos = VS.sort_videos_by_name(False)
    # sorted_videos = VS.sort_videos_by_name(True)
    sorted_videos = VS.sort_videos_by_duration(False)
    print_video_list_simple(sorted_videos)
