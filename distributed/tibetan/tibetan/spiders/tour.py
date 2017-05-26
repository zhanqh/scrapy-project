# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from tibetan.items import TibetanItem
from twisted.internet.error import TimeoutError, TCPTimedOutError


class TourSpider(RedisSpider):
    name = 'tour'
    redis_key = 'tour:start_urls'


    def parse(self, response):
        travelogues = response.xpath('//ul[@class="content"]/li')
        for travelogue in travelogues:
            url = travelogue.xpath('./div[@class="pic-box"]/a/@href').re_first(r'(http.*?html)')
            # 链接类型  a为地区论坛 o为主题论坛 c为车系论坛（车系数字为车型id）
            # 山东论坛 http://club.autohome.com.cn/bbs/thread-a-100023-36274620-1.html
            # 自驾游论坛 http://club.autohome.com.cn/bbs/thread-o-200042-36309451-1.html
            # 高尔夫论坛 http://club.autohome.com.cn/bbs/thread-c-871-35065778-1.html
            yield scrapy.Request(url, callback=self.parse_detail, errback=self.errback_timeout)

        next_page = response.urljoin(response.xpath('//a[@class="afpage"]/@href').extract_first())
        yield scrapy.Request(next_page, callback=self.parse, errback=self.errback_timeout)

    def parse_detail(self, response):
        article_url = response.url
        article_name = response.xpath('//div[@class="maxtitle"]/text()').extract_first()
        user_name = response.xpath('//*[@id="F0"]//a[@xname="uname"]/text()').extract_first()
        user_url = response.xpath('//*[@id="F0"]//a[@xname="uname"]/@href').extract_first()
        user_location = response.xpath('//*[@id="F0"]//a[contains(@title, "查看该地区论坛")]/text()').extract_first()
        post_time = response.xpath('//*[@id="F0"]//span[@xname="date"]/text()').extract_first()
        bbs_name = response.xpath('//*[@id="consnav"]/span[2]/a/text()').extract_first()
        verified_car = response.xpath('//*[@id="F0"]//a[contains(@title, "我要申请成为认证车主")]/following-sibling::node()/text()').extract()

        travelogue_item = TibetanItem()
        for field in travelogue_item.fields:
            try:
                travelogue_item[field] = eval(field)
            except NameError:
                self.logger.debug(field, '该字段没有定义')
        yield travelogue_item


    def errback_timeout(self, failure):
        self.logger.debug(repr(failure))
        if failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.debug('连接超时 %s', request.url)
            yield scrapy.Request(request.url, callback=self.parse_detail, errback=self.errback_timeout)
