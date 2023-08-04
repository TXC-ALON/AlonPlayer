import cv2
import ffmpeg
import os
from playerlib.constants import NaN
from playerlib.utils.utils import *


class Video:
    #@timer_decorator
    def __init__(self, path):
        self.path = path
        self.absolute_path = os.path.abspath(path)
        self.directory = os.path.dirname(self.absolute_path)
        self.file_name = os.path.basename(self.absolute_path)
        self.file_size_pure = os.path.getsize(self.absolute_path) / (1024 * 1024)
        self.file_size = "{:.3f}MB".format(self.file_size_pure)
        self.codec_name = None
        self.codec_long_name = None
        self.width = None
        self.height = None
        self.display_aspect_ratio = None
        self.r_frame_rate = None
        self.avg_frame_rate = None
        self.duration = NaN
        self.bit_rate = NaN
        self.color_space = None
        self.timeout = NaN
        self.overall_bit_rate = NaN
        self.__getVideoInfo()

    @timer_decorator
    def __getVideoInfo(self):
        try:
            probe = ffmpeg.probe(self.absolute_path)
            self.video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'))
        except:
            raise Exception("未找到匹配的视频流")
        # printDict(self.video_stream)
        self.codec_name = self.video_stream.get('codec_name', self.codec_name)
        self.codec_long_name = self.video_stream.get('codec_long_name', self.codec_long_name)
        self.width = self.video_stream.get('width', self.width)
        self.height = self.video_stream.get('height', self.height)
        self.display_aspect_ratio = self.video_stream.get('display_aspect_ratio', self.display_aspect_ratio)
        self.r_frame_rate = self.video_stream.get('r_frame_rate', self.r_frame_rate)
        self.avg_frame_rate = self.video_stream.get('avg_frame_rate', self.avg_frame_rate)
        self.duration = self.video_stream.get('duration', self.duration)
        self.bit_rate = self.video_stream.get('bit_rate', self.bit_rate)
        self.color_space = self.video_stream.get('color_space', self.color_space)
        self.timeout = self.__format_duration(self.duration)
        self.overall_bit_rate = self.__format_bit_rate(self.bit_rate)

    @staticmethod
    #@timer_decorator
    def __format_duration(seconds):
        return format_time(seconds)

    @staticmethod
    #@timer_decorator
    def __format_bit_rate(bit_rate):
        if bit_rate == NaN:
            return "BIT_RATE ERROR"
        bit_rate = float(bit_rate)
        if bit_rate > 1e12:
            gb, mb = divmod(bit_rate, 1e9)
            return "{:03d}.{:03d}Gb/s".format(int(gb), int(mb))
        elif bit_rate > 1e9:
            mb, kb = divmod(bit_rate, 1e6)
            return "{:03d}.{:03d}Mb/s".format(int(mb), int(kb))
        elif bit_rate > 1e3:
            kb, b = divmod(bit_rate, 1e3)
            return "{:03d}.{:03d}Kb/s".format(int(kb), int(b))
        else:
            return 'TOO LOW BIT_RATE'

    def to_dict(self):
        return vars(self)

    def print_video(self):
        print_dict(self.to_dict())

    def print_video_simple(self, order=None):
        if order is None:
            print("名称[{0}],时长=[{1}],大小=[{2}] resolution=[{3}*{4}]"
                  .format(self.file_name, self.timeout, self.file_size, self.width, self.height, order))
        else:
            print("{5}:名称[{0}],时长=[{1}],大小=[{2}] resolution=[{3}*{4}]"
                  .format(self.file_name, self.timeout, self.file_size, self.width, self.height, order))


if __name__ == '__main__':
    # testV = Video("../testfile/SongGod.mp4")
    testV = Video("../../test/testfile/Fibonacci_100.mp4")
