import random
import time

import requests
from lxml import etree

from PositionSpiderProject.conf.common import DB_MEDCHAT_NAME, PROVINCE_CITY_2018, PROVINCE_CITY_2019
from PositionSpiderProject.conf.user_agent import USER_AGENT_LIST
from PositionSpiderProject.util.mongo_util import *


class ProvinceCitySpider:

    def __init__(self, db_name, collection):
        self.mongo = DBMongo(db_name, collection)

        self.base_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/{}"
        self.start_url = self.base_url.format("index.html")
        self.headers = {}
        self.item = []

    def parse_url(self, url):  # 发送请求，获取响应
        self.headers['User-Agent'] = random.choice(USER_AGENT_LIST)
        response = requests.get(url, headers=self.headers)
        return response.content.decode("gbk", errors='ignore')

    def run(self):  # 实现主要逻辑
        province_ret_str = self.parse_url(self.start_url)

        province_html = etree.HTML(province_ret_str)
        province_hrefs = province_html.xpath("//tr[@class='provincetr']/td/a")

        # 抓取省份和下一页的链接
        for a in province_hrefs:
            province_dict = {}
            province = a.xpath("./text()")[0]
            province_link = a.xpath("./@href")[0]
            province_dict["province_name"] = province

            # 爬取市、区相关信息
            city_ret_str = self.parse_url(self.base_url.format(province_link))
            city_html = etree.HTML(city_ret_str)
            city_trs = city_html.xpath("//tr[@class='citytr']")
            city_item = []

            for city_tr in city_trs:
                city_dict = {}

                country_link = city_tr.xpath("./td[1]/a/@href")[0]
                city_code = city_tr.xpath("./td[1]/a/text()")[0]
                city_code = city_code[0:6]
                city_name = city_tr.xpath("./td[2]/a/text()")[0]
                city_dict["city_name"] = city_name
                city_dict["city_code"] = city_code
                # 爬取区县相关信息
                country_ret_str = self.parse_url(self.base_url.format(country_link))
                country_html = etree.HTML(country_ret_str)
                country_trs = country_html.xpath("//tr[@class='countytr']")
                country_item = []

                for country_tr in country_trs:
                    country_dict = {}

                    country_code = country_tr.xpath("./td[1]//text()")[0]
                    country_code = country_code[0:6]
                    country_name = country_tr.xpath("./td[2]//text()")[0]
                    country_dict["country_name"] = country_name
                    country_dict["country_code"] = country_code
                    country_item.append(country_dict)

                city_dict["country"] = country_item

                city_item.append(city_dict)

            province_dict["city"] = city_item
            self.mongo.insert_one(province_dict)
            print(province_dict)
            time.sleep(0.5)


if __name__ == '__main__':
    spider = ProvinceCitySpider(DB_MEDCHAT_NAME, PROVINCE_CITY_2019)
    spider.run()
