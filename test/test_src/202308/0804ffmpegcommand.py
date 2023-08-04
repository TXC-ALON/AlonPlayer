import subprocess
import json
from playerlib.utils.utils import *

@timer_decorator
def get_video_stream_information(file_path):
    command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', file_path]

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        output = output.decode('utf-8')
        probe_data = json.loads(output)

        video_streams = [stream for stream in probe_data['streams'] if stream['codec_type'] == 'video']

        if len(video_streams) > 0:
            return video_streams[0]
        else:
            raise Exception("未找到匹配的视频流")
    except Exception as e:
        raise e

from moviepy.editor import VideoFileClip
@timer_decorator
def get_video_stream_information2(file_path):
    try:
        video = VideoFileClip(file_path)
        video_stream = video.reader.infos
        video.close()
        return video_stream
    except Exception as e:
        raise e

# 示例调用
testVideo = (r"E:\00Learning\AlonPlayer\test\testfile\Fibonacci_100.mp4")
#video_stream_info = get_video_stream_information(testVideo)
video_stream_info = get_video_stream_information2(testVideo)
print(video_stream_info)