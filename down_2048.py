# -*- coding: utf-8 -*-
import requests, time
import random
import os
from bs4 import BeautifulSoup
from Utils import get_dir_size, get_every_max, user_agents
from down_proxy import down_load_proxy

url = 'http://www.youzi4.cc/mm/'
count_num = 3


def parse_child_page(url='', child_num=2, proxies={}, proxy_flag=False, try_time=0):
    if url == '' or url is None:
        print('地址格式不符合')
        return
    url_new = url + str(child_num) + '.html'
    headers = {
        'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
        'Referer': 'http://www.youzi4.cc/'}
    if not proxy_flag:
        try:
            child_doc = requests.get(url_new, headers=headers).text
            # time.sleep(random.randint(1, 3))
            child_soup = BeautifulSoup(child_doc, "html.parser")
            print(child_soup.img)
            pic = str(child_soup.img.get('src'))
            headers = {
                'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
                'Referer': 'http://www.youzi4.cc/'}
            r = requests.get(pic, headers=headers)
            # time.sleep(random.randint(1, 3))
            if r.status_code == 200:
                if get_dir_size('D://ss') < 100:
                    # print(pic)
                    with open('D://ss//' + pic.split('/')[-1], "wb") as p:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                p.write(chunk)
                                p.flush()
                        p.close()
        except:
            parse_child_page(url, 2, proxies, True, try_time)
    else:
        if try_time < count_num:
            try:
                parse_child_page(url, 2, proxies, False, try_time)
            except:
                parse_child_page(url, 2, proxies, False, try_time + 1)
        else:
            print('无法下载')


pp = down_load_proxy()
if not os.path.exists('D://ss'):  # 判断是否存在，如果不存在那么新建
    os.mkdir('D://ss')
for j in range(9166, 9186, 1):
    max_num = get_every_max(url, str(j))
    if max_num == 0:
        continue
    start = time.clock()
    for i in range(1, max_num + 1):
        proxies = {"http": pp[random.randint(0, len(pp) - 1)]}
        parse_child_page(url=url + str(j) + '/' + str(j) + '_', child_num=i, proxies=proxies)
    print(time.clock() - start)
