# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class EmscnuPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient('127.0.0.1', 27017)
        tdb = connection.emscnu
        self.post_info = tdb.news
    def process_item(self, item, spider):
        new = dict(item)
        self.post_info.insert(new)
        return item
