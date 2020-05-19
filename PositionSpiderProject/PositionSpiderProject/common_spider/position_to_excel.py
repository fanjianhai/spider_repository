import copy

from PositionSpiderProject.conf.common import DB_MEDCHAT_NAME, PROVINCE_CITY_2018, PROVINCE_CITY_2019, LAGOU, \
    DB_POSITION_LAGOU
from PositionSpiderProject.util.mongo_util import DBMongo
from PositionSpiderProject.util.excel_util import save_to_excel

if __name__ == '__main__':
    dbMongo = DBMongo(DB_POSITION_LAGOU, LAGOU)
    ret = dbMongo.find_no_condition()
    lst = [i for i in ret]
    save_to_excel(lst, "拉钩网爬虫", "拉钩网爬虫", "G1")
