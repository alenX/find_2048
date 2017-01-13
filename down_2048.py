# -*- coding: utf-8 -*-
import requests, time
import random
import os
import base64
import pymongo
from bs4 import BeautifulSoup
from Utils import get_dir_size, get_every_max, user_agents
from down_proxy import down_load_proxy
from threading import Thread

url = 'http://www.youzi4.cc/mm/'
count_num = 3
request_time_out = 10
local_dir = 'D://ss//dd'
client = pymongo.MongoClient("localhost", 27017)
db = client['find_2048']
info = db["bs64_info"]


def parse_child_page(url='', child_num=2, proxies={}, proxy_flag=False, try_time=1, request_time_out=10):
    if url == '' or url is None:
        print('地址格式不符合')
        return
    url_new = url + str(child_num) + '.html'
    headers = {
        'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
        'Referer': 'http://www.youzi4.cc/'}
    if not proxy_flag:
        try:
            child_doc = requests.get(url_new, headers=headers, timeout=request_time_out).text
            # time.sleep(random.randint(1, 3))
            child_soup = BeautifulSoup(child_doc, "html.parser")
            print(child_soup.img)
            pic = str(child_soup.img.get('src'))
            headers = {
                'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
                'Referer': 'http://www.youzi4.cc/'}
            r = requests.get(pic, headers=headers, timeout=request_time_out)
            # time.sleep(random.randint(1, 3))
            if r.status_code == 200:
                if get_dir_size(local_dir) < 1000:
                    # print(pic)
                    filename = local_dir + '//' + pic.split('/')[-1]
                    with open(filename, "wb") as p:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                p.write(chunk)
                                p.flush()
        except Exception as e:
            print(e)
            parse_child_page(url, child_num, proxies, True, try_time, request_time_out + 5)
    else:
        if try_time < count_num:
            try:
                child_doc = requests.get(url_new, headers=headers, proxies=proxies, timeout=request_time_out).text
                # time.sleep(random.randint(1, 3))
                child_soup = BeautifulSoup(child_doc, "html.parser")
                print('尝试次数===' + str(try_time) + child_soup.img)
                pic = str(child_soup.img.get('src'))
                headers = {
                    'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
                    'Referer': 'http://www.youzi4.cc/'}
                r = requests.get(pic, headers=headers, proxies=proxies, timeout=request_time_out)
                # time.sleep(random.randint(1, 3))
                if r.status_code == 200:
                    if get_dir_size(local_dir) < 60000:
                        # print(pic)
                        filename = local_dir + '//' + pic.split('/')[-1]
                        with open(filename, "wb") as p:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    p.write(chunk)
                                    p.flush()
            except Exception as e:
                # print(url + ' ----' + url_new + ' ---- ' + str(e))
                retry_time_out = request_time_out
                if try_time + 1 == count_num:
                    retry_time_out = request_time_out + 10
                parse_child_page(url, child_num, proxies, True, try_time + 1, retry_time_out)  # 只重采一次，增加重采时的超时时间
        else:
            pass


class down_img_thread(Thread):
    def __init__(self, url, child_num, proxies, proxy_flag, request_time_out):
        self.url = url
        self.child_num = child_num
        self.proxies = proxies
        self.proxy_flag = proxy_flag
        self.request_time_out = request_time_out
        super(down_img_thread, self).__init__()

    def run(self):
        parse_child_page(url=self.url, child_num=self.child_num, proxies=self.proxies, proxy_flag=self.proxy_flag,
                         request_time_out=self.request_time_out)


if __name__ == '__main__':
    pp = down_load_proxy()
    if not os.path.exists(local_dir):  # 判断是否存在，如果不存在那么新建
        os.mkdir(local_dir)
    for j in range(11650, 11652, 1):
        max_num = get_every_max(url, str(j))
        if max_num == 0:
            continue
        start = time.clock()
        # for i in range(1, max_num + 1):
        #     proxies = {"http": pp[random.randint(0, len(pp) - 1)]}
        #     parse_child_page(url=url + str(j) + '/' + str(j) + '_', child_num=i, proxies=proxies, proxy_flag=False,
        #                      request_time_out=10)
        # print(time.clock() - start)
        threads = []
        for i in range(1, max_num + 1):
            proxies = {
                pp[random.randint(0, len(pp) - 1)].split('=')[0]: pp[random.randint(0, len(pp) - 1)].split('=')[1]}
            t = down_img_thread(url=url + str(j) + '/' + str(j) + '_', child_num=i, proxies=proxies, proxy_flag=False,
                                request_time_out=10)
            t.start()
            threads.append(t)
            # parse_child_page()
        for t in threads:
            t.join()
        time.sleep(2)
        print(url + str(j) + '/' + str(j) + '_1.html  ' + str(time.clock() - start))
    # 将文件使用bs64写入数据库
    for each_file in os.listdir(local_dir):
        print(local_dir)
        if os.path.isfile(os.path.join(local_dir,each_file)):
            with open(local_dir + "//"+each_file, "rb") as p_p:
                mongo_pic = {'title': each_file, 'bs64': base64.b64encode(p_p.read())}
                if not info.find_one({'title': each_file}):
                    info.insert(mongo_pic)
    client.close()
