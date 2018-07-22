# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: qihu360.py 
@time: 2017/11/13 11:25

"""
import re

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings

from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.qihu360 import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


class Qihu360Spider(RedisSpider):
    name = 'qihu360_spider_redis'
    redis_key = 'qihu360_spider:start_urls'
    domain = 'http://zhushou.360.cn'

    def __init__(self, *args, **kwargs):
        super(Qihu360Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if response.url.startswith('{}/detail/index/soft_id'.format(self.domain)):
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('qihu360', 0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_xpath('app_dl_count', '//div[@id="app-info-panel"]/div/dl/dd/div/span[3]/text()')
            # 应用类型
            item_loader.add_value('app_category', 'N/A')
            # 应用名
            item_loader.add_value('app_name', re.findall("'sname': '(.*)'", response.text)[0])
            # 版本
            item_loader.add_xpath('app_version', '//div[@class="base-info"]/table/tbody/tr[2]/td[1]/text()')
            # 包名
            item_loader.add_value('app_package', re.findall("'pname': \"(.*)\"", response.text)[0])
            # 下载地址
            item_loader.add_value('app_dl_url', re.findall("'downloadUrl': '(.*)'", response.text)[0])
            yield item_loader.load_item()

        sel = Selector(response)
        links = sel.xpath('//a/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            if same_domain(url, self.domain):
                if url.startswith('{}/detail/index/soft_id'.format(self.domain)) and url.find('?recrefer') != -1:
                    url = url[0:url.find('?recrefer')]
                yield Request(url, callback=self.parse)
