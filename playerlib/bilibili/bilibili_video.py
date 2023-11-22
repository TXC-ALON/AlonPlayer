import cv2
import ffmpeg
import os

from playerlib.bilibili.utils.utils import *
from playerlib.constants import NaN
from playerlib.utils.utils import *
from bilibili_api.utils.aid_bvid_transformer import *
import asyncio
from bilibili_api import video, Credential, sync
import pandas as pd


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
    john_video = ['BV16a4y1Q7by', 'BV1na4y1Q7bD', 'BV1ey4y1c7NL', 'BV16M411X7A6', 'BV1Ez4y1F72a', 'BV1Wz4y1L7zE',
                  'BV1mk4y1w7ki', 'BV148411B7NK', 'BV1U94y147wU', 'BV1mp4y1J7Ay', 'BV1kF411Z71o', 'BV1Yr4y1o7Km',
                  'BV1dP411474Z', 'BV1SN41127Tu', 'BV1jF411Q7ke', 'BV18u411j7EX', 'BV1uk4y1u7aY', 'BV1wh4y137te',
                  'BV1sc411g7gK', 'BV1pM4y1e7Ke', 'BV1rM4y1e7XK', 'BV1No4y1G7t3', 'BV11s4y1Q7Yf', 'BV19g4y177co',
                  'BV1Qv4y177CS', 'BV1Xo4y1n7yT', 'BV1h84y1u7se', 'BV1Ug4y1W7KB', 'BV1g24y1u7Yw', 'BV1Fs4y1Z7fL',
                  'BV19s4y1b7JM', 'BV1uD4y1A7Mp', 'BV1e54y1P76A', 'BV12Y411q7S1', 'BV1A8411w723', 'BV1Z8411A74n',
                  'BV1uM411h7MN', 'BV1D44y1R7oC', 'BV1U84y147Rm', 'BV1We4y1T7Rn', 'BV1VV4y1P76f', 'BV1sP4y197HU',
                  'BV1kv4y1d7Y8', 'BV1Je4y1W7Qn', 'BV1r24y1y7r6', 'BV1cG4y147t7', 'BV1WY411Z7Cj', 'BV1QV4y1g7qH',
                  'BV1HV4y1G7sC', 'BV1Wm4y1w7F3', 'BV1R44y1f7Yv', 'BV1YN4y1N76N', 'BV1Mg411v7aE', 'BV1aV4y1N71f',
                  'BV1ge4y1y75A', 'BV1cP4y1o7G3', 'BV1Jt4y1J7wX', 'BV13W4y1t7pE', 'BV11t4y1J7wU', 'BV1cY4y1A7kj',
                  'BV1Sr4y1L7nr', 'BV1w94y1D7W8', 'BV1Rg411Z7LV', 'BV16a411S7cy', 'BV1G94y1Q75m', 'BV1h94y1X7GT',
                  'BV1Sa411W7fw', 'BV1Jr4y1G7gP', 'BV1eZ4y1q7SH', 'BV1cT411573g', 'BV1HU4y1173x', 'BV1ia411j7Eq',
                  'BV1W54y1Z7EL', 'BV1vY4y147Nk', 'BV1ZZ4y1h7f2', 'BV1o54y1f7JM', 'BV1sB4y1m73m', 'BV1s541117Hs',
                  'BV1dR4y1N7Qx', 'BV1r5411U7NV', 'BV1634y1s7GC', 'BV1x94y1f7x4', 'BV1TP4y1M7m7', 'BV1Rb4y1p7JF',
                  'BV1H44y1T74v', 'BV13Y411n7Dd', 'BV1Ha411h7pK', 'BV1Qb4y1s75W', 'BV1qa411C7ni', 'BV19F41177yJ',
                  'BV1HS4y1V7hn', 'BV1gq4y1w7pg', 'BV1c34y127nL', 'BV1KL4y1t7Do', 'BV1G44y1L7JB', 'BV1934y1z7ZQ',
                  'BV1iL411L7j2', 'BV16F411B744', 'BV1bR4y1x7RP', 'BV1444y1J7Eq', 'BV1aa411r7aQ', 'BV1Z341147jN',
                  'BV1oq4y1B7pM', 'BV1WR4y1476q', 'BV1Lh411477A', 'BV1vQ4y1U79r', 'BV1SR4y1t7jB', 'BV1fq4y1z7q1',
                  'BV1BL4y1q7NT', 'BV1pP4y1j7Lq', 'BV1zq4y1r7DW', 'BV1934y1m7x4', 'BV1mP4y1t7vp', 'BV1dq4y1o75M',
                  'BV1yL4y1z7k8', 'BV1Pq4y1o7sV', 'BV1mv411371k', 'BV1u64y1a71R', 'BV1oq4y1Z71x', 'BV1gb4y1U7vV',
                  'BV1kA411c7Ky', 'BV1iU4y1E7cV', 'BV1DM4y157xY', 'BV13h411B7AV', 'BV1P44y117HS', 'BV1a3411677R',
                  'BV11L411H7o7', 'BV1654y1n7c4', 'BV1iL411W7sC', 'BV15h411h7MF', 'BV1RX4y1A7dZ', 'BV1qM4y1u79j',
                  'BV1By4y1u7dX', 'BV1qq4y1j7Lt', 'BV1bq4y1j7pt', 'BV1v54y1L7zf', 'BV1kA411G7jg', 'BV1W64y1U71j',
                  'BV1qi4y1A76i', 'BV1ro4y1f7x4', 'BV1954y1b7N5', 'BV1nK4y1m7FT', 'BV16K4y1T76x', 'BV1UV411Y7hA',
                  'BV1Mp4y1h7ii', 'BV1Fz4y117pV', 'BV1b54y1Y72n', 'BV1Pp4y1W7rc', 'BV1oN411R7k4', 'BV1wf4y1r7sr',
                  'BV1Cf4y167A2', 'BV1Cz4y1S7M8', 'BV1ey4y1m7dc', 'BV1yU4y1x7xq', 'BV1xf4y1C7Mc', 'BV1FK4y1j7SB',
                  'BV1aA411s7i7', 'BV1Uy4y1S7Eq', 'BV11i4y1L7QQ']
    Title = []
    BV = []
    View = []
    publish_time = []
    Duration = []
    Danmaku = []
    reply = []
    like = []
    coin = []
    share = []
    for bv in john_video:
        v = BVideo(bv)
        v.get_bvideo_info()
        stat = v.stat
        Title.append(v.title)
        publish_time.append(v.ctime_h)
        Duration.append(v.time_out)
        BV.append(bv)
        View.append(stat['view'])
        Danmaku.append(stat['danmaku'])
        reply.append(stat['reply'])
        like.append(stat['like'])
        coin.append(stat['coin'])
        share.append(stat['share'])
        v.print_video_stat()

        # 创建一个DataFrame
        data = {'标题': Title,
                'BV': BV,
                '发布时间': publish_time,
                '时长': Duration,
                '播放量': View,
                '弹幕数': Danmaku,
                '评论': reply,
                '点赞': like,
                '投币': coin,
                '收藏': share,
                }
        df = pd.DataFrame(data)

        # 将DataFrame保存为Excel文件
        df.to_excel('John.xlsx', index=False)


if __name__ == '__main__':
    main()
