import ffmpeg

def get_video_info(path):
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    print(video_stream)
    if not video_stream:
        raise Exception('No video stream found')

    width = int(video_stream['width'])
    height = int(video_stream['height'])
    frame_rate = eval(video_stream['r_frame_rate'])  # 将字符串转换为小数

    return width, height, frame_rate

# 示例用法
video_path = '../../TestFile/Fibonacci_100.mp4'
width, height, frame_rate = get_video_info(video_path)

print('Width:', width)
print('Height:', height)
print('Frame Rate:', frame_rate)
