import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PositionSpiderProject.conf.user_agent import USER_AGENT_LIST

url = "https://httpbin.org/ip"
# 进入浏览器设置
options = Options()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('user-agent={}'.format(random.choice(USER_AGENT_LIST)))
options.add_argument("--proxy-server=http://113.94.123.100:4287")
# 更换头部
driver_path = r"D:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.get(url)
# 获取当前路径
print(driver.current_url)
# 网页原内容
print(driver.page_source)
i = 0
while True:
    i += 1
    options = Options()
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('--headless')
    options.add_argument('user-agent={}'.format(random.choice(USER_AGENT_LIST)))
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    if i % 2 == 0:
        options.add_argument("--proxy-server=http://1.180.165.250:4245")
    else:
        options.add_argument("--proxy-server=http://113.94.123.100:4287")

    # driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get(url)
    # 网页原内容
    print(driver.page_source)
    time.sleep(2)