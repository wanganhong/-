# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: huawei.py 
@time: 2017/11/13 11:24

"""

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings

from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.huawei import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


class HuaweiSpider(RedisSpider):
    name = 'huawei_spider_redis'
    redis_key = 'huawei_spider:start_urls'
    domain = 'http://appstore.huawei.com'

    def __init__(self, *args, **kwargs):
        super(HuaweiSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if response.url.startswith('{}/app'.format(self.domain)):
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('huawei', 0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_xpath('app_dl_count', '//span[@class="grey sub"]/text()')
            # 应用类型
            item_loader.add_value('app_category', 'N/A')
            # 应用名
            item_loader.add_xpath('app_name', '//a[@class="title"]/text()')
            # 版本
            item_loader.add_xpath('app_version', '//ul[@class="app-info-ul nofloat"]/li[4]/span/text()')
            # 包名
            item_loader.add_xpath('app_package', '//a[@class="mkapp-btn mab-download"]/@onclick')
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//a[@class="mkapp-btn mab-download"]/@onclick')
            yield item_loader.load_item()

        sel = Selector(response)
        links = sel.xpath('//a/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            if same_domain(url, self.domain):
                yield Request(url, callback=self.parse)
