# -*- coding: utf-8 -*-
import time

import scrapy


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    def __init__(self):
        self.base_get_session_url = "https://www.lagou.com/jobs/list_flink/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput="
        self.position_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"

        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://www.lagou.com/jobs/list_python?labelWords=$fromSearch=true&suginput=",
            "Host": "www.lagou.com",
        }

    def start_requests(self):
        # 设置cookie
        yield scrapy.Request(url=self.base_get_session_url, headers=self.headers, callback=self.parse_cookie_jar,
                             meta={'cookiejar': '1'})

    def parse_cookie_jar(self, response):
        for page in range(1, 2):
            data = {
                'first': 'false',
                'pn': '{}'.format(page),
                'kd': 'python'
            }
            yield scrapy.FormRequest(formdata=data, url=self.position_url, headers=self.headers, callback=self.parse_position_list,
                                 meta={'cookiejar': response.meta['cookiejar']})
            time.sleep(3)
            result = response.json()
            positions = result['content']['positionResult']['result']
            print(positions)


    def parse_position_list(self, response):
        print(response.text)
        # print(response.text)
        pass
