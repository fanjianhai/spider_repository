import base64
import random

from PositionSpiderProject.conf.user_agent import USER_AGENT_LIST


class RandomUserAgent(object):

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(USER_AGENT_LIST)


class IPProxyOpenDownloadMiddleware(object):
    """
    芝麻代理：http://h.zhimaruanjian.com/getapi/) 18210836561 fanjianhaiabc123
    链接：https://pan.baidu.com/s/1U6KnIFOYhS9NT7iXd4t84g
    """
    PROXIES = ["http://110.52.224.194:4246"]

    def process_request(self, request, spider):
        proxy = random.choice(self.PROXIES)
        request.meta['proxy'] = proxy
        print(proxy)


class IPProxyExclusiveDownloadMiddleware(object):
    """
    独享代理（快代理：https://www.kuaidaili.com/pricing/#kps）
    链接：https://pan.baidu.com/s/1U6KnIFOYhS9NT7iXd4t84g
    """
    def process_request(self,request, spider):
        proxy = '121.199.6.124:16816'
        user_password = '970138074:rcdj35ur'
        request.meta['proxy'] = proxy
        # bytes
        b64_user_password = base64.b64encode(user_password.encode("utf-8"))
        request.headers["Proxy-Authorization"] = 'Basic ' + b64_user_password.decode("utf-8")

