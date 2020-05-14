# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PositionspiderprojectItem(scrapy.Item):
    # 职位标题
    title = scrapy.Field()
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 详细地址
    address = scrapy.Field()
    # 薪水
    salary = scrapy.Field()
    # 工作经验
    experience = scrapy.Field()
    # 学历
    education = scrapy.Field()
    # 工作类型
    jobType = scrapy.Field()
    # 发布时间
    publishTime = scrapy.Field()
    # 职位诱惑
    welfare = scrapy.Field()
    # 职位职责
    jobResponsibilities = scrapy.Field()
    # 职位要求
    jobRequirements = scrapy.Field()
    # 公司名称
    companyName = scrapy.Field()
    # 公司头像
    companyIcon = scrapy.Field()
    # 公司领域
    companyField = scrapy.Field()
    # 发展阶段
    companyDevelopStage = scrapy.Field()
    # 规模
    companyScale = scrapy.Field()
    # 主页
    homePage = scrapy.Field()
    # 来源
    source = scrapy.Field()
