import random

from PositionSpiderProject.conf.user_agent import USER_AGENT_LIST


class RandomUserAgent(object):

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(USER_AGENT_LIST)
