# -*- coding: utf-8 -*-
import time
from urllib.parse import quote

import scrapy

from PositionSpiderProject.conf.common import *
import json


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Host": "www.lagou.com"
        }
        self.position_headers = {}

    def start_requests(self):
        for field in FIELDS:
            # 设置cookie
            self.position_headers[field] = {}
            self.position_headers[field]["Referer"] = INDEX_PAGE.format(quote(field))
            self.position_headers[field]["Accept"] = "application/json, text/javascript, */*; q=0.01"
            self.position_headers[field]["Host"] = "www.lagou.com"

            yield scrapy.Request(url=INDEX_PAGE.format(quote(field)), headers=self.headers,
                                 callback=self.parse_cookie_jar,
                                 meta={'cookiejar': '{}'.format(quote(field)), 'field': field})
            time.sleep(1)

    def parse_cookie_jar(self, response):
        for page in range(1, 2):
            data = {
                'first': 'false',
                'pn': '{}'.format(page),
                'kd': '{}'.format(response.meta['field'])
            }

            yield scrapy.FormRequest(formdata=data, url=LIST_PAGE,
                                     headers=self.position_headers[response.meta['field']],
                                     callback=self.parse_position_list,
                                     meta={'cookiejar': response.meta['cookiejar']})
            time.sleep(1)


    def parse_position_list(self, response):
        result = response.text
        # print(result)
        # json 转换成字典
        position_dict = json.loads(result, encoding="utf-8")
        # print(positions)
        position_items = position_dict['content']['positionResult']['result']

        for position_item in position_items:
            print(position_item['positionName'], "*****", position_item['companyFullName'])