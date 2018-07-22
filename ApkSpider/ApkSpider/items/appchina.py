# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: appchina.py 
@time: 2017/11/13 15:47

"""

import scrapy
from scrapy.loader.processors import MapCompose

from ApkSpider.utils import statistical_dl_count


def split_dl_count(value):
    temp = value.split('/')[0].strip().replace(u'下载', '').split('-')
    return statistical_dl_count(temp[1].strip() if len(temp) == 2 else temp[0].strip())


class ApkInfoItem(scrapy.Item):
    task_id = scrapy.Field()
    app_refer_url = scrapy.Field()
    app_dl_count = scrapy.Field(
        input_processor=MapCompose(split_dl_count),
    )
    app_name = scrapy.Field()
    app_category = scrapy.Field()
    app_version = scrapy.Field()
    app_package = scrapy.Field()
    app_dl_url = scrapy.Field()
    app_dl_url_hash = scrapy.Field()
