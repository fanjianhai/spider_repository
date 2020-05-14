import copy

from PositionSpiderProject.conf.common import DB_MEDCHAT_NAME, PROVINCE_CITY_2018, PROVINCE_CITY_2019
from PositionSpiderProject.util.mongo_util import DBMongo
from PositionSpiderProject.util.excel_util import save_to_excel


if __name__ == '__main__':
    dbMongo = DBMongo(DB_MEDCHAT_NAME, PROVINCE_CITY_2019)
    ret = dbMongo.find([{"$unwind": "$city"},
                            {"$group": {"_id": {"province": "$province_name", "city": "$city"}}},
                            {"$project": {"province_name": "$_id.province", "city": "$_id.city", "_id": 0}},
                            {"$unwind": {"path": "$city.country", "preserveNullAndEmptyArrays": True}}, {
                                "$project": {"province_name": 1, "city_name": "$city.city_name",
                                             "city_code": "$city.city_code",
                                             "country_name": "$city.country.country_name",
                                             "country_code": "$city.country.country_code"}},
                            {"$sort": {"province_name": 1,"city_name":1,"country_name":1}}])

    province = ""
    city_code = ""
    data_list = []
    i = 0

    for item in ret:
        print(item)
        if province != item["province_name"]:
            i = i + 1
            data_dict = copy.deepcopy({})
            # 省份不同， 写入省份
            data_dict["id"] = i
            data_dict["code"] = None
            data_dict["name"] = item["province_name"]
            data_list.append(data_dict)
            # 写入城市
            # 省份相同, 比较城市
            if city_code != item["city_code"]:
                i = i + 1
                # 城市不同，写入城市
                data_dict = copy.deepcopy({})
                data_dict["id"] = i
                data_dict["name"] = item["city_name"]
                data_dict["code"] = item["city_code"]
                data_list.append(data_dict)
                try:
                    i = i + 1
                    # 写入地区
                    data_dict = copy.deepcopy({})
                    data_dict["id"] = i
                    data_dict["name"] = item["country_name"]
                    data_dict["code"] = item["country_code"]
                    data_list.append(data_dict)
                except Exception as e:
                    print(e)

            else:
                try:
                    i = i + 1
                    # 城市相同，写入地区
                    data_dict = copy.deepcopy({})
                    data_dict["id"] = i
                    data_dict["name"] = item["country_name"]
                    data_dict["code"] = item["country_code"]
                    data_list.append(data_dict)
                except Exception as e:
                    print(e)
            city_code = item["city_code"]

        else:
            # 省份相同, 比较城市
            if city_code != item["city_code"]:
                i = i + 1
                data_dict = copy.deepcopy({})
                # 城市不同，写入城市
                data_dict["id"] = i
                data_dict["name"] = item["city_name"]
                data_dict["code"] = item["city_code"]
                data_list.append(data_dict)
                try:
                    i = i + 1
                    # 写入地区
                    data_dict = copy.deepcopy({})
                    data_dict["id"] = i
                    data_dict["name"] = item["country_name"]
                    data_dict["code"] = item["country_code"]
                    data_list.append(data_dict)
                except Exception as e:
                    print(e)
            else:
                try:
                    i = i + 1
                    # 城市相同，写入地区
                    data_dict = copy.deepcopy({})
                    data_dict["id"] = i
                    data_dict["name"] = item["country_name"]
                    data_dict["code"] = item["country_code"]
                    data_list.append(data_dict)
                except Exception as e:
                    print(e)

            city_code = item["city_code"]

        province = item["province_name"]

    save_to_excel(data_list, "2019年全国统计用区划代码和城乡划分代码", "2019年全国统计用区划代码和城乡划分代码\n\rhttp://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/","C1")


