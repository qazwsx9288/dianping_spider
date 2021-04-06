# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""
import _thread
import requests
import schedule
from faker import Factory

from utils.config import global_config


class CookieCache():
    def __init__(self):
        self.all_cookie = []
        self.valid_cookie = []
        self.invalid_cookie = []
        self.init_cookie()
        self.start_check()

    def init_cookie(self):
        """
        初始化cookie，读取文件中cookie信息，添加review、detail标记
        """
        with open('cookies.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            self.all_cookie.append([line, 0, 0])

    def get_header(self, cookie):
        ua = global_config.getRaw('config', 'user-agent')
        if ua is None:
            ua_engine = Factory.create()
            ua = ua_engine.user_agent()
        header = {
            'User-Agent': ua,
            'Cookie': cookie
        }
        return header

    def check_cookie(self):
        """
        检查cookie，定时任务，恢复&去掉 review、detail标记
        """
        review_test_url = 'http://www.dianping.com/shop/F8oeMhRBwBa99Z70/review_all/p34'
        detail_test_url = 'http://www.dianping.com/shop/G1PUPaOlLNpU8Z1h'
        for i in range(len(self.all_cookie)):
            # check detail
            r = requests.get(detail_test_url, headers=self.get_header(str(self.all_cookie[i][0]).strip()))
            if r.status_code != 200:
                self.all_cookie[i][1] = 1
            if r.status_code == 200:
                self.all_cookie[i][1] = 0
            # check review
            r = requests.get(review_test_url, headers=self.get_header(str(self.all_cookie[i][0]).strip()))
            if r.status_code != 200:
                self.all_cookie[i][2] = 1
            if r.status_code == 200:
                self.all_cookie[i][2] = 0

    def timing_check(self):
        """
        定时任务，用于定时启动check_cookie
        :return:
        """
        schedule.every().minute.at(':00').do(self.check_cookie)
        while True:
            schedule.run_pending()

    def start_check(self):
        """
        开启多线程开始cookie检查
        :return:
        """
        _thread.start_new_thread(self.timing_check, ())

    def get_cookie(self, mission_type):
        """
        获取cookie
        :param mission_type: 获取cookie所用于的任务
        :return:
        """
        assert mission_type in ['review', 'detail']
        if mission_type == 'review':
            tag = 1
        elif mission_type == 'detail':
            tag = 2
        for each in self.all_cookie:
            if each[tag] == 1:
                return each[0]
        return None

    def change_state(self, cookie, mission_type):
        """
        修改cookie状态
        :param cookie:
        :param mission_type:
        :return:
        """
        assert mission_type in ['review', 'detail']
        if mission_type == 'review':
            tag = 1
        elif mission_type == 'detail':
            tag = 2
        for each in self.all_cookie:
            if each[0] == cookie:
                each[tag] = 1


cookie_cache = CookieCache()

# def timing_check():
#     """
#     定时任务，用于定时启动check_cookie
#     :return:
#     """
#     schedule.every().minute.at(':00').do(cookie_cache.check_cookie)
#     while True:
#         schedule.run_pending()
