import re
import time

from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from PositionSpiderProject.conf.common import LAGOU, DB_POSITION_LAGOU
from PositionSpiderProject.util.mongo_util import DBMongo


class LagouSpider(object):
    """
    Selenium + ChromeDriver 拉钩爬虫
    """
    driver_path = r"D:\chromedriver\chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        # 这个链接并不是真正招聘职位信息的链接
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=$fromSearch=true&suginput='

        self.mongo = DBMongo(DB_POSITION_LAGOU, LAGOU)

    def run(self):
        self.driver.get(self.url)
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
                    WebDriverWait(self.driver, 60*60).until(
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
        position_name = htmlE.xpath("//div[@class='job-name']/h1/text()")[0]
        company = htmlE.xpath("//div[@class='job-name']/h4/text()")[0]
        job_request_spans = htmlE.xpath("//dd[@class='job_request']//span")
        salary = job_request_spans[0].xpath("./text()")[0].strip()
        salary = re.sub(r"[/ \s]", "", salary)
        city = job_request_spans[1].xpath("./text()")[0].strip()
        city = re.sub(r"[/ \s]", "", city)
        experience = job_request_spans[2].xpath("./text()")[0].strip()
        experience = re.sub(r"[/ \s]", "", experience)
        education = job_request_spans[3].xpath("./text()")[0]
        education = re.sub(r"[/ \s]", "", education)
        type = job_request_spans[4].xpath("./text()")[0]
        type = re.sub(r"[/ \s]", "", type)
        job_detail = htmlE.xpath("//div[@class='job-detail']//text()")
        job_detail = "".join(job_detail).strip()
        print("职位：%s" % position_name)
        print("单位：%s" % company)
        print("")
        print(salary + "/" + city + "/" + experience + "/" + education + "/" + type)
        print("")
        print(job_detail)

        position = {
            'name': position_name,
            'company': company,
            'salary': salary,
            'city': city,
            'experience': experience,
            'education': education,
            'desc': job_detail
        }
        print("=" * 100)

        self.mongo.insert_one(position)


if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()
