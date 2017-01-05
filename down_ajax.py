# -*- coding: utf-8 -*-
from selenium import webdriver
import time


class DownAjax(object):
    def __init__(self, url):
        self.driver = webdriver.Firefox()  # 暂时使用Firefox
        self.driver.get(url)
        self.driver.set_page_load_timeout(25)
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        # 页面初始化，加载全部页面
        height = 0
        for s in range(6):
            height += 600
            self.driver.execute_script('window.scrollTo(0,' + str(height) + ')')
            time.sleep(4)

    def down_pages(self):
        try:
            for i in range(1, 41):
                try:
                    item = self.driver.find_element_by_xpath('//*[@id="J_search_results"]/div/div[' + str(i) + ']')
                    if '立即推广' in item.text:
                        print(item.find_element_by_tag_name('img').get_attribute('src'))
                except Exception as e:
                    print(i)
                    pass
        finally:
            self.driver.close()
            self.driver.quit()


if __name__ == '__main__':
    d = DownAjax('http://pub.alimama.com/promo/item/channel/index.htm?spm=a219t.7900221/1.1998910419.ddd06e75d.lVDGCk&channel=20k')
    d.down_pages()