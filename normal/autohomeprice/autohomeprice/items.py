# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomepriceItem(scrapy.Item):
    # define the fields for your item here like:
    pid = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    verified_owner = scrapy.Field()
    post_time = scrapy.Field()
    car_model = scrapy.Field()
    invoice_price = scrapy.Field()
    msrp = scrapy.Field()
    purchase_tax = scrapy.Field()
    commercial_insurance = scrapy.Field()
    registration_cost = scrapy.Field()
    vehicle_tax = scrapy.Field()
    accidents_compulsory_insurance = scrapy.Field()
    total_price = scrapy.Field()
    others = scrapy.Field()
    promotion_package = scrapy.Field()
    buying_time = scrapy.Field()
    buying_province = scrapy.Field()
    buying_city = scrapy.Field()
    buying_shop = scrapy.Field()
    comment = scrapy.Field()
    experiences = scrapy.Field()
