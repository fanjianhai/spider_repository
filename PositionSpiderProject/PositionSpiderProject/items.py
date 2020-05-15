# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PositionspiderprojectItem(scrapy.Item):
    # 职位名称
    positionName = scrapy.Field()
    # 公司全称
    companyFullName = scrapy.Field()
    # 公司简称
    companyShortName = scrapy.Field()
    # 公司logo
    companyLogo = scrapy.Field()
    # 公司规模
    companySize = scrapy.Field()
    # 业务领域
    industryField = scrapy.Field()
    # 融资阶段
    financeStage = scrapy.Field()
    # 公司标签
    companyLabelList = scrapy.Field()
    # 第一类型
    firstType = scrapy.Field()
    # 第二类型
    secondType = scrapy.Field()
    # 第三类型
    thirdType = scrapy.Field()
    # 技能标签
    skillLables = scrapy.Field()
    # 职位标签
    positionLables = scrapy.Field()
    # 业务标签
    industryLables = scrapy.Field()
    # 创建时间（2020-05-15 15:48:30）
    createTime = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 区
    district = scrapy.Field()
    # 商业区
    businessZones = scrapy.Field()
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
    # 地铁线
    subwayline = scrapy.Field()
    #
    stationname = scrapy.Field()
    #
    linestaion = scrapy.Field()
    # 维度
    latitude = scrapy.Field()
    # 经度
    longitude = scrapy.Field()
    # 经度
    hitags = scrapy.Field()
    # 数据来源
    origin = scrapy.Field()








