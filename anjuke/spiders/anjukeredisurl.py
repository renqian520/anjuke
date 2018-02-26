# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from anjuke.items import RedisItem

class AnjukespiderSpider(CrawlSpider):
    name = 'anjukespider'
    allowed_domains = ['fang.anjuke.com']
    custom_settings = {
        'ITEM_PIPELINES':{
            'anjuke.pipelines.RedisPipeline':300,
        }
    }
    start_urls = ['https://hz.fang.anjuke.com/loupan/all/','https://hz.fang.anjuke.com/fangyuan/s?m=a']
    #楼盘页数
    loupan_page_links = LinkExtractor(allow=(r'fang.anjuke.com/loupan/all/\d+'))
    #房源页数
    fangyuan_page_links = LinkExtractor(allow=(r's?m=a&p=\d+'))
    #楼盘房源
    fangyuan_links = LinkExtractor(allow=(r'fang.anjuke.com/fangyuan/\d+.html'))
    #楼盘首页
    detail_links = LinkExtractor(allow=(r'fang.anjuke.com/loupan/\d+.html'),deny=(r'jump=site&'))
    #楼盘详情
    canshu_links = LinkExtractor(allow=(r'fang.anjuke.com/loupan/canshu-\d+.html'))
    #用户点评
    dianping_links = LinkExtractor(allow=(r'fang.anjuke.com/loupan/dianping-\d+.html'))
    dianpings_links = LinkExtractor(allow=(r'fang.anjuke.com/loupan/dianping-\d+.htmls?p=\d+'))
    #动态资讯
    officialnews_links = LinkExtractor(allow=(r'fang.anjuke.com/loupan/officialnews-\d+.html'))


    rules = (
        Rule(loupan_page_links),
        Rule(fangyuan_page_links),
        Rule(fangyuan_links, callback="parse_item", follow=True),
        Rule(detail_links,callback="parse_item",follow=True),
        Rule(canshu_links, callback="parse_item", follow=True),
        Rule(dianping_links, callback="parse_item", follow=False),
        Rule(dianpings_links, callback="parse_item", follow=False),
        Rule(officialnews_links, callback="parse_item", follow=True),

    )
    def parse_item(self, response):
        item = RedisItem()
        item['url'] = response.url
        yield item