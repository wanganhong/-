# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: appchina.py 
@time: 2017/11/13 11:32

"""

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings

from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.appchina import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


class BaiduSpider(RedisSpider):
    name = 'appchina_spider_redis'
    redis_key = 'appchina_spider:start_urls'
    domain = 'http://www.appchina.com'

    def __init__(self, *args, **kwargs):
        super(BaiduSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if response.url.startswith('{}/app/'.format(self.domain)):
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('appchina', 0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_xpath('app_dl_count', '//span[@class="app-statistic"]/text()')
            # 应用类型
            item_loader.add_xpath('app_category', '//div[@class="breadcrumb centre-content"]/a[3]/text()')
            # 应用名
            item_loader.add_xpath('app_name', '//div[@class="download-button"]/a/@meta-name')
            # 版本
            item_loader.add_xpath('app_version', '//div[@class="download-button"]/a/@meta-versionname')
            # 包名
            item_loader.add_xpath('app_package', '//div[@class="download-button"]/a/@meta-packagename')
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//div[@class="download-button"]/a/@meta-url')
            yield item_loader.load_item()

        sel = Selector(response)
        links = sel.xpath('//a/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            if same_domain(url, self.domain):
                yield Request(url, callback=self.parse)
