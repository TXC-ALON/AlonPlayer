import cv2
import ffmpeg
import os
from utils import printDict
import math
NaN = math.nan

class Video:
    def __init__(self, path):
        self.path = path
        self.absolute_path = os.path.abspath(path)
        self.directory = os.path.dirname(self.absolute_path)
        self.filename = os.path.basename(self.absolute_path)
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

    def __getVideoInfo(self):
        try:
            probe = ffmpeg.probe(self.absolute_path)
            self.video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'))
        except:
            raise Exception("未找到匹配的视频流")
        #printDict(self.video_stream)
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

    def __format_duration(self, seconds):
        if seconds == NaN:
            return "DURATION ERROR"
        seconds = float(seconds)
        seconds, milliseconds = divmod(seconds, 1)
        milliseconds *= 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:02d}:{:02d}:{:02d}:{:03d}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

    def __format_bit_rate(self, bit_rate):
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


if __name__ == '__main__':
    #testV = Video("../TestFile/SongGod.mp4")
    testV = Video("../TestFile/Fibonacci_100.mp4")
    printDict(testV.to_dict())
