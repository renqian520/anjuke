# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import redis
from scrapy.exceptions import DropItem
import anjuke.settings as settings
from anjuke.items import Mongodb_detail_Item,Mongodb_canshu_Item,Mongodb_dianping_Item,Mongodb_fangyuan_Item,Mongodb_officialnews_Item,Mongodb_news_Item

class RedisPipeline(object):
    def __init__(self):
        self.redis_db = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
        self.redis_table = settings.MY_REDIS
    def process_item(self, item, spider):
        if self.redis_db.exists(item['url']):
            raise DropItem('%s is exist!' %(item['url']))
        else:
            self.redis_db.lpush(self.redis_table,item['url'])
        return item

class MongodbPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient('mongodb://{}:{}'.format(settings.MONGODB_HOST,settings.MONGODB_PORT))
        self.db = self.conn[settings.MONGODB_DB]
        self.dc_detail = self.db[settings.MONGODB_DC_detail]
        self.dc_canshu = self.db[settings.MONGODB_DC_canshu]
        self.dc_dianping = self.db[settings.MONGODB_DC_dianping]
        self.dc_officialnews = self.db[settings.MONGODB_DC_officialnews]
        self.dc_fangyuan = self.db[settings.MONGODB_DC_fangyuan]
        self.dc_news = self.db[settings.MONGODB_DC_news]

    def process_item(self, item, spider):
        if isinstance(item,Mongodb_detail_Item):
            if self.site_detail_exist(item):
                self.dc_detail.insert(dict(item))
            else:
                raise DropItem('%s is exist!' %(item['url']))
            return item
        if isinstance(item,Mongodb_canshu_Item):
            if self.site_canshu_exist(item):
                self.dc_canshu.insert(dict(item))
            else:
                raise DropItem('%s is exist!' %(item['url']))
            return item
        if isinstance(item,Mongodb_dianping_Item):
            if self.site_dianping_exist(item):
                self.dc_dianping.insert(dict(item))
            else:
                raise DropItem('%s is exist!' %(item['content']))
            return item
        if isinstance(item,Mongodb_officialnews_Item):
            if self.site_officialnews_exist(item):
                self.dc_officialnews.insert(dict(item))
            else:
                raise DropItem('%s is exist!' %(item['news_url']))
            return item

        if isinstance(item,Mongodb_fangyuan_Item):
            if self.site_fangyuan_exist(item):
                self.dc_fangyuan.insert(dict(item))
            else:
                raise DropItem('%s is exist!' %(item['url']))
            return item

        if isinstance(item,Mongodb_news_Item):
            if self.site_news_exist(item):
                self.dc_news.insert(dict(item))
            else:
                raise DropItem('%s is exist!' %(item['url']))
            return item


    def site_detail_exist(self,item):
        if self.dc_detail.find_one({"url":item['url']}):
            return False
        else:
            return True

    def site_canshu_exist(self,item):
        if self.dc_canshu.find_one({"url":item['url']}):
            return False
        else:
            return True

    def site_dianping_exist(self, item):
        if self.dc_dianping.find_one({"content": item['content'],"url_pid":item['url_pid']}):
            return False
        else:
            return True

    def site_officialnews_exist(self,item):
        if self.dc_officialnews.find_one({"news_url":item['news_url']}):
            return False
        else:
            return True

    def site_fangyuan_exist(self,item):
        if self.dc_fangyuan.find_one({"url":item['url']}):
            return False
        else:
            return True
    def site_news_exist(self,item):
        if self.dc_news.find_one({"url":item['url']}):
            return False
        else:
            return True



