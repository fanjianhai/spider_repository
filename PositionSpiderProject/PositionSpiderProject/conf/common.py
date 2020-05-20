import datetime

time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d')
# Excel 输出路径
OUTPUT_EXCEL_DIR = r"D:\dev\spider_repository\PositionSpiderProject\PositionSpiderProject\output\excel"
EXCEL_SUFFIX = r"\{}.xlsx"
# json 输出路径
OUTPUT_JSON_DIR = r"D:\dev\spider_repository\PositionSpiderProject\PositionSpiderProject\output\json"
JSON_NAME = r"\lagou_{}.txt".format(time_str)

# Excel 输入路径
INPUT_EXCEL_DIR = r"D:\excel"
# 日志文件输出目录
LOG_FILE_DIR = r"{}\{}\logs"
LOG_FILE_SUFFIX = r"\{}.log"

# 国家统计局省市县在mongodb中数据库的名称
DB_MEDCHAT_NAME = "db_medchat"
# 国家统计局省市县在mongodb中collection的名称
PROVINCE_CITY_2018 = "province_city_2019"
PROVINCE_CITY_2019 = "province_city_2019"

# 对于一个网站需要爬取的招聘领域
# FIELDS = ['Android', '大数据', 'AI', 'Java', 'Python', 'C']
FIELDS = ['Android']

# 拉钩爬取的链接
INDEX_PAGE = "https://www.lagou.com/jobs/list_{}/p-city_0?px=new"
LIST_PAGE = "https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false"
DETAIL_PAGE = "https://www.lagou.com/jobs/{}.html"
REFFER = "https://www.lagou.com/jobs/list_{}/p-city_0?px=new"

# 国家统计局省市县在mongodb中数据库的名称
DB_POSITION_LAGOU = "db_positions_lagou"

# 国家统计局省市县在mongodb中collection的名称
LAGOU = "c_{}".format(time_str)
