import glob
from Video import *
import fnmatch
from operator import itemgetter

Default_Video_Format_List = ['.MP4', '.MKV', '.AVI', '.FLV', '.MOV', '.MPEG', '.3GP', '.WebM']


class VideoSearcher:
    def __init__(self, path, search_video_type=None, min_file_limit="1Mb"):
        if search_video_type is None:
            search_video_type = Default_Video_Format_List
        self.path = path
        self.absolute_path = os.path.abspath(path)
        self.search_type = convert_case(search_video_type)
        self.minfilelimit = parse_size_string(min_file_limit)
        self.searched_video_path = []
        self.searched_video_path = self.get_videopath()
        self.searched_video = []
        self.searched_video = self.get_video()

    def get_videopath(self):
        video_files = []
        trash_video_files = []
        folder_path = self.absolute_path
        extensions = self.search_type
        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if file_size > self.minfilelimit:  # 1MB in bytes
                        video_files.append(file_path)
                    else:
                        trash_video_files.append(file_path)

        return video_files

    def get_video(self):
        video_list = []
        for videopath in self.searched_video_path:
            temp_video = Video(videopath)
            video_list.append(temp_video)
        return video_list

    def print_searched_video(self):
        for video in self.searched_video:
            video.printvideo()

    def print_searched_video_simple(self):
        order = 1
        for video in self.searched_video:
            video.printvideo_simple(order)
            order += 1

    def sort_videos(self):
        sorted_video = sorted(self.searched_video, key=compare_video)
        return sorted_video


# def sort_videos(videos, sort_keys):
#     sorted_videos = sorted(videos, key=lambda video: [getattr(video, key[0]) for key in sort_keys])
#     for key in reversed(sort_keys):
#         if key[1]:
#             sorted_videos.reverse()
#     return sorted_videos
# def sort_videos(videos, sort_keys):
#     sorted_videos = sorted(videos, key=lambda video: [getattr(video, key[0]) for key in sort_keys])
#     for i in range(len(sort_keys)-1, -1, -1):
#         if sort_keys[i][1]:
#             sorted_videos.sort(key=lambda video: getattr(video, sort_keys[i][0]), reverse=True)
#     return sorted_videos

if __name__ == '__main__':
    VS = VideoSearcher(r"E:\00Learning\AlonPlayer")
    # print(VS.searched_video_path)

    sort_keys = [
        ('file_name', False),  # 按文件名递增排序
        ('file_size', True),  # 按文件大小递减排序
        ('duration', False)  # 按时长递增排序
    ]
    sorted_videos = sort_videos(VS.searched_video, sort_keys)
    print_video_list_simple(sorted_videos)
    for video in sorted_videos:
        print(video.file_name, video.file_size, video.duration)
    #
    # # VS = VideoSearcher(r"E:\Manim\ZA")
    # print(VS.searched_video_path)
    # print("hello world")
    # VS.print_searched_video_simple()
    # sortedVS = VS.sort_videos()
    # print_video_list_simple(sortedVS)
