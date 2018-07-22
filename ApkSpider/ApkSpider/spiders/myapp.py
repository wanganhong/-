# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: myapp.py 
@time: 2017/11/13 11:30

"""

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings

from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.myapp import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


# TODO 应用宝（myapp）反爬虫校验，需要加代理
class MyappSpider(RedisSpider):
    name = 'myapp_spider_redis'
    redis_key = 'myapp_spider:start_urls'
    domain = 'http://android.myapp.com'

    def __init__(self, *args, **kwargs):
        super(MyappSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if response.url.find(r'detail.htm?apkName=') != -1:
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('myapp', 0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_xpath('app_dl_count', '//div[@class="det-ins-num"]/text()')
            # 应用类型
            item_loader.add_xpath('app_category', '//a[@class="det-type-link"]/text()')
            # 应用名
            item_loader.add_xpath('app_name', '//div[@class="det-ins-btn-box"]/a[@class="det-ins-btn"]/@appname')
            # 版本
            item_loader.add_xpath('app_version',
                                  '//div[@data-modname="appOthInfo"]/div[@class="det-othinfo-data"]/text()')
            # 包名
            item_loader.add_xpath('app_package', '//div[@class="det-ins-btn-box"]/a[@class="det-ins-btn"]/@apk')
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//div[@class="det-ins-btn-box"]/a[@class="det-ins-btn"]/@ex_url')
            yield item_loader.load_item()

        sel = Selector(response)
        links = sel.xpath('//a/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            if same_domain(url, self.domain):
                yield Request(url, callback=self.parse)
