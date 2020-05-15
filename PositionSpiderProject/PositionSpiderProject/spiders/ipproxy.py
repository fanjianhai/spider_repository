# -*- coding: utf-8 -*-
import json

import scrapy


class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']

    def start_requests(self):
        # 设置cookie
        yield scrapy.Request(url="http://httpbin.org/user-agent", callback=self.parse, dont_filter=False)

    def parse(self, response):
        # origin = json.loads(response.text)['user-agent']
        # print("*" * 10)
        # print(origin)
        print(response.text)
