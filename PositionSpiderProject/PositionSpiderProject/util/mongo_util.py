from pymongo import MongoClient
from PositionSpiderProject.util.excel_util import save_to_excel


class DBMongo:
    """
    Mongo 数据库操作工具类
    """

    def __init__(self, db_name, collection_name, host="192.168.1.27", port=27017):
        self.__client = MongoClient(host, port)
        self.__collection = self.__client[db_name][collection_name]

    @property
    def client(self):
        return self.__client

    @property
    def collection(self):
        return self.__collection

    def insert_one(self, value):
        self.__collection.insert_one(value)

    def insert_many(self, value):
        self.__collection.insert_many(value)

    def find_no_condition(self):
        return self.__collection.aggregate([{"$project": {"_id": 0}}])

    def find(self, aggregation_condition: list):
        return self.__collection.aggregate(aggregation_condition)


if __name__ == '__main__':
    dbMongo = DBMongo("db_test", "test")
    # dbMongo.insert_one({"name": "小海", "age": 28,"sex":"female"})
    rets = dbMongo.find()
    data_list = [i for i in rets]
    save_to_excel(data_list, "2019年省市县列表汇总", "2019年省市县列表汇总", "C1")
