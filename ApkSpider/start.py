# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: start.py 
@time: 2017/11/13 14:12

"""

from scrapy.cmdline import execute


def run():
    # execute('scrapy crawl anzhi_spider_redis'.split())
    # execute('scrapy crawl appchina_spider_redis'.split())
    # execute('scrapy crawl baidu_spider_redis'.split())
    # execute('scrapy crawl huawei_spider_redis'.split())
    # execute('scrapy crawl myapp_spider_redis'.split())
    # execute('scrapy crawl pp_spider_redis'.split())
    # execute('scrapy crawl qihu360_spider_redis'.split())
    # execute('scrapy crawl xiaomi_spider_redis'.split())
    # execute('scrapy crawl wandoujia_spider_redis'.split())
    execute('scrapy crawl mumayi_spider_redis'.split())

if __name__ == '__main__':
    run()
