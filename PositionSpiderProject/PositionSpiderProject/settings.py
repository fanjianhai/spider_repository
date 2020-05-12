# 1.导包
import logging
import datetime
import os


# 2.项目名称
BOT_NAME = 'PositionSpiderProject'

# 3.模块名称
SPIDER_MODULES = ['{}.spiders'.format(BOT_NAME)]
NEWSPIDER_MODULE = '{}.spiders'.format(BOT_NAME)

# 4.遵守机器人协议（默认为True）
ROBOTSTXT_OBEY = False


# 5.格式化日志输出的格式，日志文件每分钟生成一个文件
time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M')
LOG_FILE = '{}\\{}\\logs\\{}.log'.format(os.getcwd(), BOT_NAME, time_str)
LOG_LEVEL = 'DEBUG'

# 6.设置运行多个爬虫的自定义命令
COMMANDS_MODULE = '{}.commands'.format(BOT_NAME)

# 7.scrapy输出的json文件中显示中文（https://www.cnblogs.com/linkr/p/7995454.html）
FEED_EXPORT_ENCODING = 'utf-8'

# 8.管道pipeline配置，后面的值越小，越先经过这根管道
ITEM_PIPELINES = {
   '{}.pipelines.PositionspiderprojectPipeline'.format(BOT_NAME): 300,
}

# 9.限制爬虫的爬取速度， 单位为秒
DOWNLOAD_DELAY = 1

# 10. 下载中间件
DOWNLOADER_MIDDLEWARES = {
   '{}.middlewares.RandomUserAgent'.format(BOT_NAME): 1,
}

# 11. 禁用cookie
COOKIES_ENABLED = False
