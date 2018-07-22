# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
import redis
from scrapy.exceptions import DropItem
from scrapy.conf import settings

from ApkSpider.utils import get_hash


class DuplicatePipeline(object):
    def __init__(self):
        self.redis = redis.Redis(
            host=settings['REDIS_HOST'],
            port=settings['REDIS_PORT'],
            password=settings['REDIS_PARAMS']['password'],
            db=0)

    def process_item(self, item, spider):
        try:
            app_pkg = item['app_package']
        except KeyError:
            raise DropItem('Package not found in page!')
        if app_pkg is None:
            raise DropItem('Package not found in page!')
        if self.redis.sismember("app_packages", app_pkg):
            raise DropItem('Package:<{}> already exist!'.format(app_pkg))
        self.redis.sadd("app_packages", app_pkg)
        return item


class AnzhispiderPipeline(object):
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = pymysql.Connect(
            db=settings['MYSQL_DBNAME'],
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8'
        )
        self.conn.autocommit(True)
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.save_item(item)
        return item

    def save_item(self, item):
        self.insert(proc='pro_sp_random_download_task_add_new',
                    args=(
                        item['task_id'],
                        item['app_dl_url'],
                        get_hash(item['app_dl_url']),
                        item['app_refer_url'],
                        item['app_category'],
                        item['app_name'],
                        item['app_dl_count'],
                        item['app_version'],
                        item['app_package']

                    ))

    def insert(self, proc, args):
        self.connect()
        try:
            self.cur.callproc(proc, args)
            self.conn.commit()
        except Exception as e:
            print e
        finally:
            self.close()
