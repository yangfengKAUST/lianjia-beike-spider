#!/usr/bin/env python
# coding=utf-8

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.xiaoqu import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *

class StockBaseSpider(BaseSpider):
    # def collect_area_xiaoqu_data(self, stock_code, fmt="csv"):
    #     csv_file = self.today_path + "/{0}.csv".format(stock_code)
    #     with open(csv_file, "w") as f:
    #         # 开始获得需要的板块数据
    #         xqs = self.get_stock_info(stock_code)
    #         # 锁定
    #         if self.mutex.acquire(1):
    #             self.total_num += len(xqs)
    #             # 释放
    #             self.mutex.release()
    #         if fmt == "csv":
    #             for xiaoqu in xqs:
    #                 f.write(self.date_string + "," + xiaoqu.text() + "\n")
    #     print("Finish crawl area: " + area_name + ", save data to : " + csv_file)
    #     logger.info("Finish crawl area: " + area_name + ", save data to : " + csv_file)


    @staticmethod
    def get_stock_info(stock_code):
        total_page = 1

        xiaoqu_list = list()
        # page = 'http://{0}.{1}.com/xiaoqu/{2}/'.format(city, SPIDExR_NAME, area)
        page = 'http://stock.finance.sina.com.cn/hkstock/finance/{0}'.format(stock_code)
        print(page)
        logger.info(page)

        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
            print('the num of total page {0}'.format(total_page))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(stock_code))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        for i in range(1, total_page + 1):
            headers = create_headers()
            page = 'http://{0}.{1}.com/xiaoqu/{2}/pg{3}'.format(city, SPIDER_NAME, area, i)
            print(page)  # 打印版块页面地址
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elems = soup.find_all('li', class_="xiaoquListItem")
            for house_elem in house_elems:
                price = house_elem.find('div', class_="totalPrice")
                name = house_elem.find('div', class_='title')
                on_sale = house_elem.find('div', class_="xiaoquListItemSellCount")

                # 继续清理数据
                price = price.text.strip()
                name = name.text.replace("\n", "")
                on_sale = on_sale.text.replace("\n", "").strip()

                # 作为对象保存
                xiaoqu = XiaoQu(chinese_district, chinese_area, name, price, on_sale)
                xiaoqu_list.append(xiaoqu)
        return xiaoqu_list


if __name__ == '__main__':
    test = StockBaseSpider(SPIDER_NAME)
    test.get_stock_info('00700')