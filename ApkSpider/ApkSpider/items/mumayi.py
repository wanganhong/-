# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: mumayi.py 
@time: 2017/12/14 15:08

"""

import scrapy
from scrapy.loader.processors import MapCompose


def split_pkg(value):
    return value if value.find('.') != -1 else None


def split_name(value):
    return value.split()[0]


def split_version(value):
    return value.split()[1]


class ApkInfoItem(scrapy.Item):
    task_id = scrapy.Field()
    app_refer_url = scrapy.Field()
    app_dl_count = scrapy.Field()
    app_name = scrapy.Field(
        input_processor=MapCompose(split_name),
    )
    app_category = scrapy.Field()
    app_version = scrapy.Field(
        input_processor=MapCompose(split_version),
    )
    app_package = scrapy.Field(
        input_processor=MapCompose(split_pkg),
    )
    app_dl_url = scrapy.Field()
    app_dl_url_hash = scrapy.Field()

