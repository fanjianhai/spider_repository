import re
import time

from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from PositionSpiderProject.conf.common import LAGOU, DB_POSITION_LAGOU, OUTPUT_JSON_DIR, JSON_NAME, INDEX_PAGE, FIELDS
from PositionSpiderProject.util.mongo_util import DBMongo
import json
import os
from urllib.parse import quote


class LagouSpider(object):
    """
    Selenium + ChromeDriver 拉钩爬虫
    """
    driver_path = r"D:\chromedriver\chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        # 这个链接并不是真正招聘职位信息的链接
        # self.url = 'https://www.lagou.com/jobs/list_python?labelWords=$fromSearch=true&suginput='

        self.mongo = DBMongo(DB_POSITION_LAGOU, LAGOU)

        if not os.path.exists(OUTPUT_JSON_DIR):
            os.makedirs(OUTPUT_JSON_DIR)

    def run(self):
        self.driver.get(INDEX_PAGE.format(quote(FIELDS[0])))
        while True:
            time.sleep(2)
            source = self.driver.page_source
            try:
                self.driver.find_element_by_xpath("//div[@class='qr_code_content']")
                continue
            except NoSuchElementException as e:
                pass

            WebDriverWait(self.driver, 7).until(
                # 这里只能追踪的元素，不能追踪到元素的具体属性
                EC.presence_of_element_located((By.XPATH, "//div[@class='pager_container']/span[last()]"))
            )
            self.parse_list_page(source)
            next_btn = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
            if "pager_next_disabled" in next_btn.get_attribute("class"):
                break
            else:
                try:
                    next_btn.click()
                except Exception as e:
                    WebDriverWait(self.driver, 60 * 60).until(
                        # 这里只能追踪的元素，不能追踪到元素的具体属性
                        EC.presence_of_element_located((By.XPATH, "//div[@class='pager_container']/span[last()]"))
                    )

    def parse_list_page(self, source):
        """解析列表"""
        htmlE = etree.HTML(source)
        links = htmlE.xpath("//a[@class='position_link']/@href")
        self.request_detail_page(links)

    def request_detail_page(self, urls):

        current_page = 0

        for i in range(len(urls)):
            time.sleep(2)

            self.driver.execute_script("window.open('{}')".format(urls[current_page]))
            self.driver.switch_to.window(self.driver.window_handles[1])

            try:
                self.driver.find_element_by_xpath("//div[@class='qr_code_content']")
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                continue
            except NoSuchElementException as e:
                pass

            WebDriverWait(self.driver, 7).until(
                # EC.presence_of_element_located((By.XPATH, "//div[@class='job-name']/@title"))
                # 这里只能追踪到元素，追踪不到元素下的具体属性
                EC.presence_of_element_located((By.XPATH, "//div[@class='job-name']"))
            )

            page_srouce = self.driver.page_source
            self.parse_detail_page(page_srouce)
            # 关闭这个详情页
            self.driver.close()
            # 继续切换到职位列表页面
            self.driver.switch_to.window(self.driver.window_handles[0])
            current_page += 1

    def parse_detail_page(self, source):
        htmlE = etree.HTML(source)
        positionName = htmlE.xpath("//div[@class='job-name']/h1/text()")[0]
        companyName = htmlE.xpath("//div[@class='job-name']/h4/text()")[0]
        companyE = htmlE.xpath("//h4[@class='c_feature_name']//text()")
        print(len(companyE))
        companySize = companyE[len(companyE) - 2].strip()
        industryField = companyE[0].strip()
        financeStage = companyE[1].strip()
        companyLink = companyE[len(companyE) - 1].strip()
        job_request_spans = htmlE.xpath("//dd[@class='job_request']//span")
        city = job_request_spans[1].xpath("./text()")[0].strip()
        city = re.sub(r"[/ \s]", "", city)
        salary = job_request_spans[0].xpath("./text()")[0].strip()
        salary = re.sub(r"[/ \s]", "", salary)
        workYear = job_request_spans[2].xpath("./text()")[0].strip()
        workYear = re.sub(r"[/ \s]", "", workYear)
        education = job_request_spans[3].xpath("./text()")[0]
        education = re.sub(r"[/ \s]", "", education)
        jobNature = job_request_spans[4].xpath("./text()")[0]
        jobNature = re.sub(r"[/ \s]", "", jobNature)
        positionAdvantage = htmlE.xpath("//dd[@class='job-advantage']//text()")
        positionAdvantage = "".join(positionAdvantage).strip()
        jobDetail = htmlE.xpath("//div[@class='job-detail']//text()")
        jobDetail = "".join(jobDetail).strip()
        workAddr = htmlE.xpath("//div[@class='work_addr']//text()")
        workAddr = "".join(workAddr).strip()
        workAddr = re.sub(r"[查看地图 \s]", "", workAddr)

        position = {
            'positionName': positionName,
            'companyName': companyName,
            'companySize': companySize,
            'industryField': industryField,
            'financeStage': financeStage,
            'companyLink': companyLink,
            'city': city,
            'salary': salary,
            'workYear': workYear,
            'education': education,
            'jobNature': jobNature,
            'positionAdvantage': positionAdvantage,
            'jobDetail': jobDetail,
            'workAddr': workAddr,
            'origin': "拉钩网",
        }
        print(position)
        print("=" * 100)

        with open(OUTPUT_JSON_DIR + JSON_NAME, "a", encoding="utf-8") as fp:
            fp.write(json.dumps(position, ensure_ascii=False) + "\n")

        self.mongo.insert_one(position)


if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()
