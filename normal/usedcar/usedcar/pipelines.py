# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from usedcar.items import UsedcarItem


class UsedcarPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, UsedcarItem):
            if not item.get('associate_new_car'):
                item['associate_new_car'] = False
            if not item.get('warranty_period'):
                item['warranty_period'] = False
        return item

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_tb):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_tb = mongo_tb

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB'),
            mongo_tb = crawler.settings.get('MONGO_TB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[self.mongo_tb].update({'infoid': item.get('infoid')}, {'$set': dict(item)}, True)
        return item

    def close_spider(self, spider):
        self.client.close()
