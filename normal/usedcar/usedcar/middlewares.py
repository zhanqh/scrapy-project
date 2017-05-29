# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import redis
import random
from scrapy import signals


class UsedcarSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):

    def __init__(self, proxy_pool_url, proxy_pool_port, proxy_pool_password):
        if proxy_pool_password:
            self.db = redis.Redis(host=proxy_pool_url, port=proxy_pool_port, password=proxy_pool_password)
        else:
            self.db = redis.Redis(host=proxy_pool_url, port=proxy_pool_port)

    def _get_random_proxy(self):
        try:
            if self.db.keys('proxy:1:*'):
                proxy = self.db.get(random.choice(self.db.keys('proxy:1:*')))
            else:
                proxy = self.db.get(random.choice(self.db.keys('proxy:2:*')))
            return (proxy).decode('ascii')
        except Exception:
            return None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_pool_url=crawler.settings.get('PROXY_POOL_URL'),
            proxy_pool_port=crawler.settings.get('PROXY_POOL_PORT'),
            proxy_pool_password=crawler.settings.get('PROXY_POOL_PASSWORD')
        )

    def process_request(self, request, spider):
        proxy = self._get_random_proxy()
        if proxy:
            request.meta['proxy'] = proxy
            spider.logger.debug('使用代理：' + proxy)
        else:
            spider.logger.debug('没有可使用的代理')

    def process_response(self, request, response, spider):
        if response.status is 429:
            request.meta['proxy'] = self._get_random_proxy()
            return request
        else:
            return response
