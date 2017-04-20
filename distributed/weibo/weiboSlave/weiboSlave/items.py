# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboslaveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment_id = scrapy.Field()
    name = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()
    reply_text = scrapy.Field()
    reply_name = scrapy.Field()
