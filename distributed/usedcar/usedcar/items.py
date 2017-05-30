# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UsedcarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    infoid = scrapy.Field()
    url = scrapy.Field()
    car = scrapy.Field()
    mileage = scrapy.Field()
    registration_time = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    new_car_tax_price = scrapy.Field()
    associate_new_car = scrapy.Field()
    warranty_period = scrapy.Field()
