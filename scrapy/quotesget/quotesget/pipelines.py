# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.exceptions import DropItem
from .items import ZHUserArticlesItem, ZHUserItem
from scrapy import crawler

class QuotesgetPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):

        if item['text']:
            if len(item['text']) > self.limit:
                #to limit the length of text and trip the kongge and add ...
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing text...')

class MongoDBPipeline(object):
    def __init__(self, mongo_host, mongo_db):
        self.monggo_host = mongo_host
        self.monggo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        #???
        return cls(
            mongo_host = crawler.settings.get('MONGGO_HOST'),
            mongo_db = crawler.settings.get('MONGGO_DB')
    )

    #when the spider begins, this function will be ran
    def open_spider(self, spider):

        self.client = pymongo.MongoClient(self.monggo_host)
        self.db = self.client[self.monggo_db]

    #proccess item
    def process_item(self, item, spider):
        #get the spider's name
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    #to close the mongodb
    def close_spider(self, spider):
        self.client.close()


    #enable the pipline


class MySQLPipeline(object):
    def __init__(self, host, user, password, db, port):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        #self.sql = 'insert into quotes(`text`,`author`,`tags`) values(%s, %s, %s)'
        self.sql = 'insert into quotes(`text`,`author`,`tags`) values("{}", "{}", "{}")'


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            user = crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            db = crawler.settings.get('MYSQL_DB'),
            port = crawler.settings.get('MYSQL_PORT')
        )
    def open_spider(self, spider):
        self.connect = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(self.sql.format(str(item['text']), str(item['author']), str(item['tags'])))
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()

class PspgameSavePipline(object):
    def __init__(self, host, user, password, db, port):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        # self.sql = 'insert into quotes(`text`,`author`,`tags`) values(%s, %s, %s)'
        self.sql_6 = 'insert into pspgame(`name`,`type`,`maker`, `release_time`, `stars`, `details`) values("{}", "{}", "{}", "{}", "{}", "{}")'
        self.sql_7 = 'insert into pspgame(`name`,`type`,`maker`, `release_time`, `version`, `stars`, `details`) values("{}", "{}", "{}", "{}", "{}", "{}", "{}")'
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            user = crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            db = crawler.settings.get('MYSQL_DB'),
            port = crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        self.connect = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        if len(item) == 6:
            self.cursor.execute(self.sql_6.format(str(item['name']), str(item['type']), item['maker'], item['release_time'], str(item['stars']), item['details']))
            self.connect.commit()
        if len(item) == 7:
            self.cursor.execute(self.sql_7.format(str(item['name']), str(item['type']), item['maker'], item['release_time'], item['version'], str(item['stars']), item['details']))
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()

class PspgamePipline(object):
    def __init__(self):
        self.cut_common_words = 5
        self.cut_stars_words = 6

    def process_item(self, item, spider):
        # item['name'] = str(item['name'][self.cut_common_words:])

        # to cut the chinese characters
        item['type'] = str(item['type'][self.cut_common_words:])
        item['maker'] = str(item['maker'][self.cut_common_words:])
        item['release_time'] = str(item['release_time'][self.cut_common_words:])
        item['version'] = str(item['version'][self.cut_common_words:])
        item['details'] = str(item['details'][self.cut_common_words:])
        return item


class ZHUserSaveToMysqlPipline(object):
    def __init__(self, host, user, password, db, port):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.sql = ''
        self.connect = ''
        self.cursor = ''

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            user = crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            db = crawler.settings.get('MYSQL_DB'),
            port = crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        self.connect = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        pass

    def close_spider(self, spider):
        self.connect.close()


class ZHUserSaveToMonggoPipline(object):
    def __init__(self, monggo_host, monggo_db):
        self.monggo_host = monggo_host
        self.monggo_db = monggo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            monggo_host=crawler.settings.get('MONGGO_HOST'),
            monggo_db=crawler.settings.get('MONGGO_DB')
        )

    def open_spider(self, spider):
        # link to client
        # self.client = pymongo.MongoClient(self.monggo_host)

        self.client = pymongo.MongoClient(self.monggo_host)
        self.db = self.client[self.monggo_db]
        # choose or create db
        # self.db = self.client[self.monggo_db]

    def process_item(self, item, spider):

        if isinstance(item, ZHUserItem):
            name = item.__class__.__name__
            # self.db[name].insert(dict(item))
            # delete the complex items
            self.db[name].update({'name': item['url_token']}, {'$set': item}, True)
        return item

    def close_spider(self, spider):
        self.client.close()

class ZHUserArticlesSaveToMonggoPipline(object):
    def __init__(self, monggo_host, monggo_db):
        self.monggo_host = monggo_host
        self.monggo_db = monggo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            monggo_host=crawler.settings.get('MONGGO_HOST'),
            monggo_db=crawler.settings.get('MONGGO_DB')
        )

    def open_spider(self, spider):
        # link to client
        # self.client = pymongo.MongoClient(self.monggo_host)

        self.client = pymongo.MongoClient(self.monggo_host)
        self.db = self.client[self.monggo_db]
        # choose or create db
        # self.db = self.client[self.monggo_db]

    def process_item(self, item, spider):
        # name = item.__class__.__name__
        if isinstance(item, ZHUserArticlesItem):
            name = item.__class__.__name__
            self.db[name].insert({'name':item['author']['name']}, {'$set':item})

        # delete the complex items
        # self.db[name].update({'name': item['author']['name']}, {'$set': item}, True)
        return item

    def close_spider(self, spider):
        self.client.close()


