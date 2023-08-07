import cv2
import ffmpeg
import os

from playerlib.bilibili.utils.utils import *
from playerlib.constants import NaN
from playerlib.utils.utils import *
from bilibili_api.utils.aid_bvid_transformer import *
import asyncio
from bilibili_api import video, Credential, sync


class BVideo:
    def __init__(self, _bvid):
        self.dms = None
        self.stat = None
        self.owner = None
        self.pubdate = None
        self.dimension = None
        self.time_out = None
        self.duration = None
        self.desc = None
        self.type = None
        self.ctime_h = None
        self.pubdate_h = None
        self.ctime = None
        self.title = None
        self.videoinfo = None
        self.bvid = _bvid
        self.aid = bvid2aid(self.bvid)
        self.v = video.Video(bvid=self.bvid)

    def get_bvideo_info(self) -> None:
        self.videoinfo = sync(self.v.get_info())
        self.title = self.videoinfo['title']
        self.type = self.videoinfo['tname']
        self.pubdate = self.videoinfo['pubdate']
        self.ctime = self.videoinfo['ctime']
        self.pubdate_h = convert_pubdate(self.pubdate)
        self.ctime_h = convert_pubdate(self.ctime)
        self.duration = self.videoinfo['duration']
        self.time_out = format_time(self.duration)
        self.dimension = self.videoinfo['dimension']
        self.owner = self.videoinfo['owner']
        self.stat = self.videoinfo['stat']

    def to_dict(self):
        return vars(self)

    def print_owner_info(self):
        return print_owner_info(self.owner)

    def print_video_stat(self):
        stat = self.stat
        if stat is not None:
            print("Up[{8}]--[{7}] : 播放量 {0} 弹幕量 {1} 评论数 {2} 点赞{3} 投币{4} 收藏{5} 分享{6} "
                  .format(stat['view'], stat['danmaku'], stat['reply'], stat['like'],
                          stat['coin'], stat['favorite'], stat['share'], self.title, self.owner['name']))

    def get_damuku(self, _limit=10):
        limit = _limit
        dms = sync(self.v.get_danmakus(0))
        self.dms = dms[:limit]
        print("弹幕数量为{0}".format(len(dms)))
        for dm in self.dms:
            print_single_damu(dm)


def main() -> None:
    v = BVideo("BV11X4y17722")
    v.get_bvideo_info()
    v.print_video_stat()
    v.get_damuku(20)


if __name__ == '__main__':
    main()
