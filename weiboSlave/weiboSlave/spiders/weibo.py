# -*- coding: utf-8 -*-
import scrapy


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["http://m.weibo.cn"]
    start_urls = ['http://http://m.weibo.cn/']

    def parse(self, response):
        pass
