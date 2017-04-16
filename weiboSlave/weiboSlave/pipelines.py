# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class WeibomasterPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient('10.104.152.137', 27017)
        tdb = connection.weibo
        self.post_info = tdb.comments
    def process_item(self, item, spider):
        comment = dict(item)
        self.post_info.insert(comment)
        return item
