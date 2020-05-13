from pymongo import MongoClient


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

    def find(self):
        return self.__collection.find()


if __name__ == '__main__':
    dbMongo = DBMongo("db_test", "test")
    # dbMongo.insert_one({"name": "小范", "age": 29, "hobbies": ["NBA", "乒乓球", "旅行"]})
    rets = dbMongo.find()
    for ret in rets:
        print(ret)
