# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: anzhi.py 
@time: 2017/11/13 11:31

"""

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings

from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.anzhi import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


class AnZhiSpider(RedisSpider):
    name = "anzhi_spider_redis"
    redis_key = "anzhi_spider:start_urls"
    domain = "http://www.anzhi.com"

    def __init__(self, *args, **kwargs):
        super(AnZhiSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        sel = Selector(response)
        if response.url.startswith('http://www.anzhi.com/pkg') or response.url.startswith('http://www.anzhi.com/soft'):
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('anzhi', 0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_xpath('app_dl_count', '//ul[@id="detail_line_ul"]/li[2]/span/text()')
            # 应用类型
            item_loader.add_xpath('app_category', '//div[@class="title"]/h2/a/text()')
            # 应用名
            item_loader.add_xpath('app_name', '//div[@class="title"]/h3/text()')
            # 版本
            item_loader.add_xpath('app_version',
                                  '//div[@class="detail_description"]/div[@class="detail_line"]/span[@class="app_detail_version"]/text()')
            # 包名
            item_loader.add_xpath('app_package', '//div[@class="detail_icon"]/ul/li[2]/a/@href')
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//div[@class="detail_other"]/div[@class="detail_down"]/a/@onclick')
            yield item_loader.load_item()

        links = sel.xpath('//a/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            # if same_domain(url, self.domain) and url.find("author_list.php?auth=") == -1:
            if same_domain(url, self.domain):
                yield Request(url, callback=self.parse)
