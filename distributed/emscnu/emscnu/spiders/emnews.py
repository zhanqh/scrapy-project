# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from emscnu.items import EmscnuItem
from redis import Redis


class EmnewsSpider(RedisSpider):
    name = "emnews"
    redis_key = 'myspider:start_urls'
    # allowed_domains = ["em.scnu.edu.cn"]
    # start_urls = ['http://em.scnu.edu.cn/xueyuanxinwen/index.html']

    def parse(self, response):
        if response.status is 200:
            print(response.url + ' ✓done!')
            news = EmscnuItem()

            for li in response.css('div.c_news ul li'):
                news['title'] = li.css('a::text').extract_first()
                yield news
                
        else:
            print('response error')
