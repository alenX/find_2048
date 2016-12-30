# -*- coding: utf-8 -*-
import requests, time
import random
import os
from bs4 import BeautifulSoup
from Utils import get_dir_size, get_every_max, user_agents
from down_proxy import down_load_proxy
from threading import Thread

url = 'http://www.youzi4.cc/mm/'
count_num = 3
request_time_out = 10
local_dir = 'F://ss'


def parse_child_page(url='', child_num=2, proxies={}, proxy_flag=False, try_time=0, request_time_out=10):
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
                    with open(local_dir + '//' + pic.split('/')[-1], "wb") as p:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                p.write(chunk)
                                p.flush()
                        p.close()
        except:
            parse_child_page(url, child_num, proxies, True, try_time, request_time_out)
    else:
        if try_time < count_num:
            try:
                child_doc = requests.get(url_new, headers=headers, proxies=proxies, timeout=request_time_out).text
                # time.sleep(random.randint(1, 3))
                child_soup = BeautifulSoup(child_doc, "html.parser")
                print(child_soup.img)
                pic = str(child_soup.img.get('src'))
                headers = {
                    'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
                    'Referer': 'http://www.youzi4.cc/'}
                r = requests.get(pic, headers=headers, proxies=proxies, timeout=request_time_out)
                # time.sleep(random.randint(1, 3))
                if r.status_code == 200:
                    if get_dir_size(local_dir) < 60000:
                        # print(pic)
                        with open(local_dir + '//' + pic.split('/')[-1], "wb") as p:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    p.write(chunk)
                                    p.flush()
                            p.close()
            except:
                parse_child_page(url, child_num, proxies, False, try_time + 1, request_time_out)
        else:
            print('无法下载')


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
    for j in range(8607, 9006, 1):
        max_num = get_every_max(url, str(j))
        if max_num == 0:
            continue
        start = time.clock()
        threads = []
        for i in range(1, max_num + 1):
            proxies = {"http": pp[random.randint(0, len(pp) - 1)]}
            t = down_img_thread(url=url + str(j) + '/' + str(j) + '_', child_num=i, proxies=proxies, proxy_flag=False,
                             request_time_out=10)
            t.start()
            threads.append(t)
            # parse_child_page()
        for t in threads:
            t.join()
        print(time.clock() - start)
