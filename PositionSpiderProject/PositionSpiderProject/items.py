# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PositionSpiderProjectItem(scrapy.Item):
    # 职位名称
    positionName = scrapy.Field()
    # 公司名称
    companyName = scrapy.Field()
    # 公司规模
    companySize = scrapy.Field()
    # 业务领域
    industryField = scrapy.Field()
    # 融资阶段
    financeStage = scrapy.Field()
    # 公司官网
    companyLink = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 工作年限
    workYear = scrapy.Field()
    # 工作性质
    jobNature = scrapy.Field()
    # 教育
    education = scrapy.Field()
    # 职位优势
    positionAdvantage = scrapy.Field()
    # 工作详情
    jobDetail = scrapy.Field()
    # 工作地点
    workAddr = scrapy.Field()
    # 数据来源
    origin = scrapy.Field()








