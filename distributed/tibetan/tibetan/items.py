# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TibetanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_url = scrapy.Field()
    article_name = scrapy.Field()
    user_name = scrapy.Field()
    user_url = scrapy.Field()
    user_location = scrapy.Field()
    post_time = scrapy.Field()
    bbs_name = scrapy.Field()
    verified_car = scrapy.Field()
