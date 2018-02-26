# -*- coding: utf-8 -*-
import scrapy
from anjuke.items import RedisItem
import re


class AnjukesnewsSpider(scrapy.Spider):
    name = 'anjukenews'
    allowed_domain = 'news.anjuke.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'anjuke.pipelines.RedisPipeline': 300,
        }
    }
    start_urls = ['https://hz.news.anjuke.com/toutiao/ajax/toutiaoajax/?page=1&type=1']
    def parse(self, response):
        try:
            urls = re.compile('"url":"(.*?)","', re.S).findall(str(response.text).replace('\\',''))
            for url in urls:
                item = RedisItem()
                if len(url):
                    item['url'] = url
                else:
                    pass
                yield item
        except:
            pass


        for i in range(1,600):
            url = 'https://hz.news.anjuke.com/toutiao/ajax/toutiaoajax/?page={}&type=1'.format(str(i))
            if url:
                yield scrapy.Request(url,callback=self.parse,dont_filter=True)


