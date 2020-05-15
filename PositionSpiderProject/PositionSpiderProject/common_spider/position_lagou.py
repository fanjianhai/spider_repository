import requests
from lxml import etree
import time
import re

# 请求头
HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Referer": "https://www.lagou.com/jobs/list_python?labelWords=$fromSearch=true&suginput=",
    "Host": "www.lagou.com",
}


def request_list_page():
    url0 = "https://www.lagou.com/jobs/list_flink/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput="
    url1 = 'https://www.lagou.com/jobs/list_python'

    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    # 通过data来控制翻页

    s = requests.Session()  # 建立session
    s.get(url=url1, headers=HEADERS, timeout=3)

    for page in range(1, 10):
        data = {
            'first': 'false',
            'pn': page,
            'kd': 'python'
        }
        respon = s.post(url=url, headers=HEADERS, data=data, timeout=3)
        time.sleep(3)
        result = respon.json()
        positions = result['content']['positionResult']['result']
        print(positions)
        # for position in positions:
        #     positionId = position['positionId']
        #     position_url = "https://www.lagou.com/jobs/{}.html".format(positionId)
        #     parse_position_detail(position_url, s)
        #     break


def parse_position_detail(url, s):
    response = s.get(url, headers=HEADERS)
    text = response.text
    htmlE = etree.HTML(text)
    position_name = htmlE.xpath("//div[@class='job-name']/@title")[0]
    job_request_spans = htmlE.xpath("//dd[@class='job_request']//span")
    salary = job_request_spans[0].xpath("./text()")[0].strip()
    education = job_request_spans[3].xpath("./text()")[0]
    education = re.sub(r"[/ \s]", "", education)
    job_detail = htmlE.xpath("//div[@class='job-detail']//text()")
    job_detail = "".join(job_detail).strip()


if __name__ == '__main__':
    request_list_page()
