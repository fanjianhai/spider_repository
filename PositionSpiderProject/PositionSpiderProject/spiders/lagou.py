# -*- coding: utf-8 -*-
import scrapy
import logging


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        logging.debug("=" * 50)
        logging.debug(response.text)
        logging.debug("=" * 50)