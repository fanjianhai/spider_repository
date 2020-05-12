# -*- coding: utf-8 -*-
import scrapy
import logging


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://lagou.com/']

    def parse(self, response):
        logging.debug("=" * 50)
        logging.debug(response.text)
        logging.debug("=" * 50)