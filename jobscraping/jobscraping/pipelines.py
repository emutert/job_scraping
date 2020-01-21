# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo

class MongoPipeline(object):

    
    def __init__(self, mongo_uri, mongo_db , mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_col = crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post
        self.db[self.mongo_col].insert(dict(item))
        logging.debug("Post added to MongoDB")
        return item




"""
import pymongo

# Scrapy 1.0+ proper settings access
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        return item"""


"""         
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
            if valid:
                self.collection.insert(dict(iter))
                log.msg("Job added to DB",
                level=log.DEBUG, spider=spider) 
            return item"""
