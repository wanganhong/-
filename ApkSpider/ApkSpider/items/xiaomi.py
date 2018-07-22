# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: xiaomi.py 
@time: 2017/11/13 17:05

"""

import scrapy
from scrapy.loader.processors import MapCompose


def split_dl_url(value):
    return u'http://app.mi.com/download/{}'.format(value)


class ApkInfoItem(scrapy.Item):
    task_id = scrapy.Field()
    app_refer_url = scrapy.Field()
    app_dl_count = scrapy.Field()
    app_name = scrapy.Field()
    app_category = scrapy.Field()
    app_version = scrapy.Field()
    app_package = scrapy.Field()
    app_dl_url = scrapy.Field(
        input_processor=MapCompose(split_dl_url),
    )
    app_dl_url_hash = scrapy.Field()
