import timeit

from bilibili_api import user, Credential, login, sync
import asyncio

from playerlib import print_dict, timer_decorator

bili_jct = "4ae51ba6596d0bf6473a93627b1d5f01"
SESSDATA = r"4d37b749%2C1706772054%2Cead83%2A82IZadUGIuOuZdu15Yv0d7ZPM5Hm_MInpIgy0VxAXGZJZD8qLjwS15QQhz_gPk7hSV_zEwIQAANAA"
buvid3 = "51D3A445-9731-4292-D8A3-D0D1E38DE34634473infoc"

Alon_CREDENTIAL = Credential(
    sessdata=SESSDATA,
    bili_jct=bili_jct,
    buvid3=buvid3
)


class BUser_simple:
    def __init__(self, _uid, _follower_num, _name):
        self.b_user = None
        self.uid = _uid
        self.follower = _follower_num
        self.name = _name


class BUser:
    def __init__(self, _uid: int):
        self.video_info = None
        self.uid = _uid
        self.face = None
        self.sex = None
        self.name = None
        self.info = None
        self.b_user = None
        self.follower_num = None
        self.following_num = None
        self.relation_info = None
        self.all_following = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.Bilibili_user_init())

    @timer_decorator
    async def Bilibili_user_init(self):
        self.b_user = user.User(uid=self.uid)
        self.info = await self.return_user_info()
        self.relation_info = await self.b_user.get_relation_info()
        self.name = self.info['name']
        self.sex = self.info['sex']
        self.face = self.info['face']
        self.following_num = self.relation_info['following']
        self.all_following = await self.b_user.get_all_followings()
        self.follower_num = self.relation_info['follower']
        #self.video_info = await self.b_user.get_videos()

    async def return_user_info(self):
        info = await self.b_user.get_user_info()
        return info

    def print_user_info(self):
        print("{0}({1})    关注数{2}".format(self.name, self.uid, self.follower_num))

    @timer_decorator
    def get_following_userinfo(self):
        following_user_list = []
        for user_id in self.all_following[:5]:
            temp_user = BUser(user_id)
            following_user_list.append(temp_user)
        sorted_following_user_list = sorted(following_user_list, key=lambda x: x.follower_num)
        return sorted_following_user_list


async def check_same_followers() -> None:
    CREDENTIAL = Alon_CREDENTIAL
    stn = user.User(uid=7349, credential=CREDENTIAL)
    #stn_info = await stn.get_user_info()
    # print(stn_info)

    lists = await stn.get_self_same_followers()
    for up in lists["list"]:
        print(up["uname"], end=" ")


@timer_decorator
def test():

    start_time = timeit.default_timer()
    # 你的代码行
    stn = BUser(7349)
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    stn_video_info = stn.video_info
    print(stn_video_info)


if __name__ == '__main__':
    test()
    # #print_dict(stn.info)
    #
    #
    # print(stn.name)
    # print(stn.relation_info)
    # tomato = BUser(546195)
    # print(tomato.relation_info)
    # print(stn.all_following)
    # # print_dict(tomato.info)
    # # asyncio.run(check_same_followers())
