# -*- coding: utf-8 -*-
from anjuke.items import Mongodb_detail_Item,Mongodb_canshu_Item,Mongodb_dianping_Item,Mongodb_officialnews_Item,Mongodb_fangyuan_Item,Mongodb_news_Item
from scrapy_redis.spiders import RedisSpider
import re
import scrapy

class Myspider(RedisSpider):
    name = 'mongodburl'
    custom_settings = {
        'ITEM_PIPELINES':{
            'anjuke.pipelines.MongodbPipeline':300,
        }
    }
    redis_key = 'anjuke_news_spider:start_urls'


    def parse(self, response):
        try:
            item_detail = Mongodb_detail_Item()
            item_canshu = Mongodb_canshu_Item()
            item_dianping = Mongodb_dianping_Item()
            item_officialnews = Mongodb_officialnews_Item()
            item_fangyuan =  Mongodb_fangyuan_Item()
            item_news = Mongodb_news_Item()
            # 楼盘首页
            if 'canshu' not in response.url and 'jump' not in response.url and 'dianping' not in response.url and 'officialnews' not in response.url and 'fangyuan' not in response.url and 'news' not in response.url:
                item_detail['url'] = response.url
                item_detail['url_pid'] = str(item_detail['url']).split('/')[-1].split('.')[0]
                item_detail['img'] = self.get_img(response)
                item_detail['leimu'] = self.get_leimu(response)
                yield item_detail
            #楼盘详情
            if 'canshu' in response.url:
                print('*****************'+ response.url)
                item_canshu['url'] = response.url
                item_canshu['url_pid'] = str(item_canshu['url']).split('/')[-1].split('.')[0].split('-')[1]
                item_canshu['name'] = self.get_name(response)
                item_canshu['tedian'] = self.get_tedian(response)
                item_canshu['singleprice'] = self.get_singleprice(response)
                item_canshu['allprice'] = self.get_allprice(response)
                item_canshu['leixing'] = self.get_leixing(response)
                item_canshu['developers'] = self.get_developers(response)
                item_canshu['quyu'] = self.get_quyu(response)
                item_canshu['dizhi'] = self.get_dizhi(response)
                item_canshu['dianhua'] = self.get_dianhua(response)
                item_canshu['shoufu'] = self.get_shoufu(response)
                item_canshu['yuegong'] = self.get_yuegong(response)
                item_canshu['huxing'] = self.get_huxing(response)
                item_canshu['kaipan'] = self.get_kaipan(response)
                item_canshu['shijian'] = self.get_shijian(response)
                item_canshu['shouloudizhi'] = self.get_shouloudizhi(response)
                item_canshu['xukezheng'] = self.get_xukezheng(response)
                item_canshu['jianzuleixing'] = self.get_jianzuleixing(response)
                item_canshu['nianxian'] = self.get_nianxian(response)
                item_canshu['rongji'] = self.get_rongji(response)
                item_canshu['lvhua'] = self.get_lvhua(response)
                item_canshu['hushu'] = self.get_hushu(response)
                item_canshu['louceng'] = self.get_louceng(response)
                item_canshu['guanli'] = self.get_guanli(response)
                item_canshu['wuye'] = self.get_wuye(response)
                item_canshu['chewei'] = self.get_chewei(response)
                item_canshu['cheweibi'] = self.get_cheweibi(response)
                yield item_canshu
            # 用户点评
            if 'dianping' in response.url:
                item_dianping['url'] = response.url
                item_dianping['url_pid'] = str(item_dianping['url']).split('/')[-1].split('.')[0].split('-')[1]
                yield scrapy.Request(item_dianping['url'],meta={'item_dianping':item_dianping},callback=self.parse_dianping)
            # 动态资讯
            if 'officialnews' in response.url:
                item_officialnews['url'] = response.url
                item_officialnews['url_pid'] = str(item_officialnews['url']).split('/')[-1].split('.')[0].split('-')[1]
                yield scrapy.Request(item_officialnews['url'], meta={'item_officialnews': item_officialnews},
                                     callback=self.parse_officialnews)
            # 楼盘房源
            if 'fangyuan' in response.url:
                item_fangyuan['url'] = response.url
                item_fangyuan['url_pid'] = str(item_fangyuan['url']).split('/')[-1].split('.')[0]
                item_fangyuan['fang_title'] = self.get_fang_title(response)
                item_fangyuan['fang_shoujia'] = self.get_fang_shoujia(response)
                item_fangyuan['fang_fangxing'] = self.get_fang_fangxing(response)
                item_fangyuan['fang_youhui'] = self.get_fang_youhui(response)
                item_fangyuan['fang_mianji'] = self.get_fang_mianji(response)
                item_fangyuan['fang_shoufu'] = self.get_fang_shoufu(response)
                item_fangyuan['fang_chaoxiang'] = self.get_fang_chaoxiang(response)
                item_fangyuan['fang_yuegong'] = self.get_fang_yuegong(response)
                item_fangyuan['fang_louceng'] = self.get_fang_louceng(response)
                item_fangyuan['fang_leixing'] = self.get_fang_leixing(response)
                item_fangyuan['fang_zhuangxiu'] = self.get_fang_zhuangxiu(response)
                item_fangyuan['fang_dizhi'] = self.get_fang_dizhi(response)
                item_fangyuan['fang_shijian'] = self.get_fang_shijian(response)
                yield item_fangyuan
            # 楼讯
            if 'news' in response.url and 'huabao' not in response.url:
                item_news['url'] = response.url
                item_news['news_title'] = self.get_news_title(response)
                item_news['news_pubtime'] = self.get_news_pubtime(response)
                item_news['news_content'] = self.get_news_content(response)
                yield item_news
        except IndexError:
            pass

    # 楼盘
    def get_img(self,response):
        li = []
        img = re.compile('<img width="86" height="63" src="(.*?)">').findall(response.text)
        for i in img:
            if len(i):
                li.append(i)
                img = ','.join(li)
            else:
                img = 'NULL'
        return img
    def get_leimu(self,response):
        li = []
        leimu = re.compile('soj="loupan_index_crumb">(.*?)</a>').findall(response.text)
        for i in leimu:
            if len(i):
                li.append(i)
                leimu = '>'.join(li)
            else:
                leimu = 'NULL'
        return leimu

    # 楼盘参数
    def get_name(self,response):
        try:
            name = re.compile('楼盘名称</div>(.*?)</div>',re.S).findall(response.text)
            for i in name:
                if len(i):
                    name = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;','',str(i))).strip().replace(' ','')
                    name = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '',str(name))).strip().replace(' ', '')
                else:
                    name = 'NULL'
                return name
            if len(name) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_tedian(self,response):
        try:
            li = []
            tedian = re.compile('soj="canshu_left_tips">(.*?)</a>').findall(response.text)
            for i in tedian:
                if len(tedian):
                    li.append(i)
                    tedian = '|'.join(li)
                else:
                    tedian = 'NULL'
            return tedian
        except:
            return 'NULL'
    def get_singleprice(self,response):
        try:
            singleprice = re.compile('参考单价</div>(.*?)</div>',re.S).findall(response.text)
            for i in singleprice:
                if len(i):
                    singleprice = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;','',str(i))).strip().replace(' ','')
                    singleprice = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(singleprice))).strip().replace(' ', '')
                else:
                    singleprice = 'NULL'
                return singleprice
            if len(singleprice) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_allprice(self,response):
        try:
            allprice = re.compile('楼盘总价</div>(.*?)</div>', re.S).findall(response.text)
            for i in allprice:
                if len(i):
                    allprice = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    allprice = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(allprice))).strip().replace(' ', '')
                else:
                    allprice = 'NULL'
                return allprice
            if len(allprice) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_leixing(self,response):
        try:
            leixing = re.compile('物业类型</div>(.*?)</div>', re.S).findall(response.text)
            for i in leixing:
                if len(i):
                    leixing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    leixing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(leixing))).strip().replace(' ', '')
                else:
                    leixing = 'NULL'
                return leixing
            if len(leixing) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_developers(self,response):
        try:
            developers = re.compile('开发商</div>(.*?)</div>', re.S).findall(response.text)
            for i in developers:
                if len(i):
                    developers = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    developers = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(developers))).strip().replace(' ', '')
                else:
                    developers = 'NULL'
                return developers
            if len(developers) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_quyu(self,response):
        try:
            quyu = re.compile('区域位置</div>(.*?)</div>', re.S).findall(response.text)
            for i in quyu:
                if len(i):
                    quyu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    quyu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(quyu))).strip().replace(' ', '')
                else:
                    quyu = 'NULL'
                return quyu
            if len(quyu) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_dizhi(self,response):
        try:
            dizhi = re.compile('楼盘地址</div>(.*?)</div>', re.S).findall(response.text)
            for i in dizhi:
                if len(i):
                    dizhi = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    dizhi = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(dizhi))).strip().replace(' ', '')
                else:
                    dizhi = 'NULL'
                return dizhi
            if len(dizhi) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_dianhua(self,response):
        try:
            dianhua = re.compile('售楼处电话</div>(.*?)</div>', re.S).findall(response.text)
            for i in dianhua:
                if len(i):
                    dianhua = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    dianhua = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(dianhua))).strip().replace(' ', '')
                else:
                    dianhua = 'NULL'
                return dianhua
            if len(dianhua) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_shoufu(self,response):
        try:
            shoufu = re.compile('最低首付</div>(.*?)</div>', re.S).findall(response.text)
            for i in shoufu:
                if len(i):
                    shoufu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    shoufu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(shoufu))).strip().replace(' ', '')
                else:
                    shoufu = 'NULL'
                return shoufu
            if len(shoufu) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_yuegong(self,response):
        try:
            yuegong = re.compile('月供</div>(.*?)</div>', re.S).findall(response.text)
            for i in yuegong:
                if len(i):
                    yuegong = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    yuegong = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(yuegong))).strip().replace(' ', '')
                else:
                    yuegong = 'NULL'
                return yuegong
            if len(yuegong) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_huxing(self,response):
        try:
            huxing = re.compile('楼盘户型</div>(.*?)</div>', re.S).findall(response.text)
            for i in huxing:
                if len(i):
                    huxing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    huxing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(huxing))).strip().replace(' ', '')
                else:
                    huxing = 'NULL'
                return huxing
            if len(huxing) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_kaipan(self,response):
        try:
            kaipan = re.compile('最新开盘</div>(.*?)</div>', re.S).findall(response.text)
            for i in kaipan:
                if len(i):
                    kaipan = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    kaipan = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(kaipan))).strip().replace(' ', '')
                else:
                    kaipan = 'NULL'
                return kaipan
            if len(kaipan) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_shijian(self,response):
        try:
            shijian = re.compile('交房时间</div>(.*?)</div>', re.S).findall(response.text)
            for i in shijian:
                if len(i):
                    shijian = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;|&emsp;', '', str(i))).strip().replace(' ','')
                    shijian = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;|&emsp;', '', str(shijian))).strip().replace(' ', '')
                else:
                    shijian = 'NULL'
                return shijian
            if len(shijian) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_shouloudizhi(self,response):
        try:
            shouloudizhi = re.compile('售楼处地址</div>(.*?)</div>', re.S).findall(response.text)
            for i in shouloudizhi:
                if len(i):
                    shouloudizhi = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    shouloudizhi = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(shouloudizhi))).strip().replace(' ', '')
                else:
                    shouloudizhi = 'NULL'
                return shouloudizhi
            if len(shouloudizhi) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_xukezheng(self,response):
        try:
            xukezheng = re.compile('预售许可证</div>(.*?)</div>', re.S).findall(response.text)
            for i in xukezheng:
                if len(i):
                    xukezheng = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    xukezheng = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(xukezheng))).strip().replace(' ', '')
                else:
                    xukezheng = 'NULL'
                return xukezheng
            if len(xukezheng) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_jianzuleixing(self,response):
        try:
            jianzuleixing = re.compile('建筑类型</div>(.*?)</div>', re.S).findall(response.text)
            for i in jianzuleixing:
                if len(i):
                    jianzuleixing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    jianzuleixing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(jianzuleixing))).strip().replace(' ', '')
                else:
                    jianzuleixing = 'NULL'
                return jianzuleixing
            if len(jianzuleixing) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_nianxian(self,response):
        try:
            nianxian = re.compile('产权年限</div>(.*?)</div>', re.S).findall(response.text)
            for i in nianxian:
                if len(i):
                    nianxian = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    nianxian = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(nianxian))).strip().replace(' ', '')
                else:
                    nianxian = 'NULL'
                return nianxian
            if len(nianxian) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_rongji(self,response):
        try:
            rongji = re.compile('容积率</div>(.*?)</div>', re.S).findall(response.text)
            for i in rongji:
                if len(i):
                    rongji = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    rongji = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(rongji))).strip().replace(' ', '')
                else:
                    rongji = 'NULL'
                return rongji
            if len(rongji) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_lvhua(self,response):
        try:
            lvhua = re.compile('绿化率</div>(.*?)</div>', re.S).findall(response.text)
            for i in lvhua:
                if len(i):
                    lvhua = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    lvhua = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(lvhua))).strip().replace(' ', '')
                else:
                    lvhua = 'NULL'
                return lvhua
            if len(lvhua) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_hushu(self,response):
        try:
            hushu = re.compile('规划户数</div>(.*?)</div>', re.S).findall(response.text)
            for i in hushu:
                if len(i):
                    hushu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    hushu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(hushu))).strip().replace(' ', '')
                else:
                    hushu = 'NULL'
                return hushu
            if len(hushu) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_louceng(self,response):
        try:
            louceng = re.compile('楼层状况</div>(.*?)</div>', re.S).findall(response.text)
            for i in louceng:
                if len(i):
                    louceng = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    louceng = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(louceng))).strip().replace(' ', '')
                else:
                    louceng = 'NULL'
                return louceng
            if len(louceng) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_guanli(self,response):
        try:
            guanli = re.compile('物业管理费</div>(.*?)</div>', re.S).findall(response.text)
            for i in guanli:
                if len(i):
                    guanli = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    guanli = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(guanli))).strip().replace(' ', '')
                else:
                    guanli = 'NULL'
                return guanli
            if len(guanli) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_wuye(self,response):
        try:
            wuye = re.compile('物业公司</div>(.*?)</div>', re.S).findall(response.text)
            for i in wuye:
                if len(i):
                    wuye = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    wuye = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(wuye))).strip().replace(' ', '')
                else:
                    wuye = 'NULL'
                return wuye
            if len(wuye) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_chewei(self,response):
        try:
            chewei = re.compile('车位数</div>(.*?)</div>', re.S).findall(response.text)
            for i in chewei:
                if len(i):
                    chewei = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    chewei = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(chewei))).strip().replace(' ', '')
                else:
                    chewei = 'NULL'
                return chewei
            if len(chewei) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_cheweibi(self,response):
        try:
            cheweibi = re.compile('车位比</div>(.*?)</div>', re.S).findall(response.text)
            for i in cheweibi:
                if len(i):
                    cheweibi = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    cheweibi = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(cheweibi))).strip().replace(' ', '')
                else:
                    cheweibi = 'NULL'
                return cheweibi
            if len(cheweibi) == 0:
                return 'NULL'
        except:
            return 'NULL'

    # 楼盘点评
    def parse_dianping(self,response):
        item_dianping = response.meta['item_dianping']
        try:
            for box in response.xpath('//div[@class="info-mod"]'):
                content = box.xpath('.//h4[@class="rev-subtit all-text"]/text()').extract()
                if len(content):
                    item_dianping['content'] = content[0]
                else:
                    item_dianping['content'] = 'NULL'
                pubtime = box.xpath('.//span[@class="date"]/text()').extract()
                if len(pubtime):
                    item_dianping['pubtime'] = pubtime[0]
                else:
                    item_dianping['pubtime'] = 'NULL'
                author = box.xpath('.//span[@class="author"]/text()').extract()
                if len(author):
                    item_dianping['author'] = author[0]
                else:
                    item_dianping['author'] = 'NULL'
                yield item_dianping
        except IndexError:
            pass

    # 楼盘动态资讯
    def parse_officialnews(self,response):
        item_officialnews = response.meta['item_officialnews']
        try:
            for box in response.xpath('//div[@class="r_invite"]/b'):
                news_url = box.xpath('.//a/@href').extract()[0]
                yield scrapy.Request(news_url,callback=self.parse_officialnews_url,meta={'item_officialnews':item_officialnews})
        except IndexError:
            pass
    def parse_officialnews_url(self,response):
        item_officialnews = response.meta['item_officialnews']
        try:
            item_officialnews['news_url'] = response.url
            for box in response.xpath('//div[@class="news-detail"]'):
                item_officialnews['title'] = box.xpath('.//h1/text()').extract()[0]
                item_officialnews['pubtime'] = box.xpath('.//div[@class="tit-sub gray"]/span/text()').extract()[0]
                item_officialnews['content'] = str(box.xpath('string(.//div[@class="infos"]/p)').extract()[0]).strip().replace('\r|\t','')
                yield item_officialnews
        except IndexError:
            pass


    #楼盘房源
    def get_fang_title(self,response):
        try:
            title = re.compile('<h2 class="fy-title">(.*?)</h2>', re.S).findall(response.text)
            for i in title:
                if len(i):
                    title = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ','')
                    title = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(title))).strip().replace(' ', '')
                else:
                    title = 'NULL'
                return title
            if len(title) == 0:
                title_a = re.compile('<h2>(.*?)</h2>', re.S).findall(response.text)
                for i in title_a:
                    if len(i):
                        title_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        title_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(title_a))).strip().replace(' ', '')
                    else:
                        title_a = 'NULL'
                    return title_a
                if len(title_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_fang_shoujia(self, response):
        try:
            shoujia = re.compile('售价</span>(.*?)</span>', re.S).findall(response.text)
            for i in shoujia:
                if len(i):
                    shoujia = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    shoujia = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(shoujia))).strip().replace(' ', '')
                else:
                    shoujia = 'NULL'
                return shoujia
            if len(shoujia) == 0:
                shoujia_a = re.compile('<b class="i0 i1">(.*?)</i>', re.S).findall(response.text)
                for i in shoujia_a:
                    if len(i):
                        shoujia_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        shoujia_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(shoujia_a))).strip().replace(' ', '')
                    else:
                        shoujia_a = 'NULL'
                    return shoujia_a
                if len(shoujia_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_fang_fangxing(self, response):
        try:
            fangxing = re.compile('房型</span>(.*?)</span>', re.S).findall(response.text)
            for i in fangxing:
                if len(i):
                    fangxing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    fangxing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(fangxing))).strip().replace(' ', '')
                else:
                    fangxing = 'NULL'
                return fangxing
            if len(fangxing) == 0:
                fangxing_a = re.compile('房型：(.*?)<em>', re.S).findall(response.text)
                for i in fangxing_a:
                    if len(i):
                        fangxing_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        fangxing_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(fangxing_a))).strip().replace(' ', '')
                    else:
                        fangxing_a = 'NULL'
                    return fangxing_a
                if len(fangxing_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_fang_youhui(self, response):
        try:
            youhui = re.compile('优惠</span>(.*?)</span>', re.S).findall(response.text)
            for i in youhui:
                if len(i):
                    youhui = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    youhui = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(youhui))).strip().replace(' ', '')
                else:
                    youhui = 'NULL'
                return youhui
            if len(youhui) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_fang_mianji(self, response):
        try:
            mianji = re.compile('面积</span>(.*?)</span>', re.S).findall(response.text)
            for i in mianji:
                if len(i):
                    mianji = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    mianji = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(mianji))).strip().replace(' ', '')
                else:
                    mianji = 'NULL'
                return mianji
            if len(mianji) == 0:
                mianji_a = re.compile('<li>面积：(.*?)</li>', re.S).findall(response.text)
                for i in mianji_a:
                    if len(i):
                        mianji_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        mianji_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(mianji_a))).strip().replace(' ', '')
                    else:
                        mianji_a = 'NULL'
                    return mianji_a
                if len(mianji_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_fang_shoufu(self, response):
        try:
            shoufu = re.compile('参考首付</span>(.*?)</span>', re.S).findall(response.text)
            for i in shoufu:
                if len(i):
                    shoufu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    shoufu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(shoufu))).strip().replace(' ', '')
                else:
                    shoufu = 'NULL'
                return shoufu
            if len(shoufu) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_fang_chaoxiang(self, response):
        try:
            chaoxiang = re.compile('朝向</span>(.*?)</span>', re.S).findall(response.text)
            for i in chaoxiang:
                if len(i):
                    chaoxiang = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    chaoxiang = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(chaoxiang))).strip().replace(' ', '')
                else:
                    chaoxiang = 'NULL'
                return chaoxiang
            if len(chaoxiang) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_fang_yuegong(self, response):
        try:
            yuegong = re.compile('参考月供</span>(.*?)</span>', re.S).findall(response.text)
            for i in yuegong:
                if len(i):
                    yuegong = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    yuegong = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(yuegong))).strip().replace(' ', '')
                else:
                    yuegong = 'NULL'
                return yuegong
            if len(yuegong) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_fang_louceng(self, response):
        try:
            louceng = re.compile('楼层</span>(.*?)</span>', re.S).findall(response.text)
            for i in louceng:
                if len(i):
                    louceng = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    louceng = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(louceng))).strip().replace(' ', '')
                else:
                    louceng = 'NULL'
                return louceng
            if len(louceng) == 0:
                louceng_a = re.compile('楼层：(.*?)<em>', re.S).findall(response.text)
                for i in louceng_a:
                    if len(i):
                        louceng_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        louceng_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(louceng_a))).strip().replace(' ', '')
                    else:
                        louceng_a = 'NULL'
                    return louceng_a
                if len(louceng_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_fang_leixing(self, response):
        try:
            leixing = re.compile('物业类型</span>(.*?)</span>', re.S).findall(response.text)
            for i in leixing:
                if len(i):
                    leixing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    leixing = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(leixing))).strip().replace(' ', '')
                else:
                    leixing = 'NULL'
                return leixing
            if len(leixing) == 0:
                leixing_a = re.compile('物业类型：(.*?)</li>', re.S).findall(response.text)
                for i in leixing_a:
                    if len(i):
                        leixing_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        leixing_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(leixing_a))).strip().replace(' ', '')
                    else:
                        leixing_a = 'NULL'
                    return leixing_a
                if len(leixing_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_fang_zhuangxiu(self, response):
        try:
            zhuangxiu = re.compile('装修</span>(.*?)</span>', re.S).findall(response.text)
            for i in zhuangxiu:
                if len(i):
                    zhuangxiu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    zhuangxiu = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(zhuangxiu))).strip().replace(' ', '')
                else:
                    zhuangxiu = 'NULL'
                return zhuangxiu
            if len(zhuangxiu) == 0:
                zhuangxiu_a = re.compile('<em>装修：(.*?)</em>', re.S).findall(response.text)
                for i in zhuangxiu_a:
                    if len(i):
                        zhuangxiu_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        zhuangxiu_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(zhuangxiu_a))).strip().replace(' ', '')
                    else:
                        zhuangxiu_a = 'NULL'
                    return zhuangxiu_a
                if len(zhuangxiu_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_fang_dizhi(self, response):
        try:
            dizhi = re.compile('地址</span>(.*?)</span>', re.S).findall(response.text)
            for i in dizhi:
                if len(i):
                    dizhi = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    dizhi = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(dizhi))).strip().replace(' ', '')
                else:
                    dizhi = 'NULL'
                return dizhi
            if len(dizhi) == 0:
                dizhi_a = re.compile('"li1">地址：(.*?)</li>', re.S).findall(response.text)
                for i in dizhi_a:
                    if len(i):
                        dizhi_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        dizhi_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(dizhi_a))).strip().replace(' ', '')
                    else:
                        dizhi_a = 'NULL'
                    return dizhi_a
                if len(dizhi_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_fang_shijian(self, response):
        try:
            shijian = re.compile('交房时间</span>(.*?)</span>', re.S).findall(response.text)
            for i in shijian:
                if len(i):
                    shijian = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    shijian = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(shijian))).strip().replace(' ', '')
                else:
                    shijian = 'NULL'
                return shijian
            if len(shijian) == 0:
                shijian_a = re.compile('开盘时间：(.*?)</li>', re.S).findall(response.text)
                for i in shijian_a:
                    if len(i):
                        shijian_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        shijian_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(shijian_a))).strip().replace(' ', '')
                    else:
                        shijian_a = 'NULL'
                    return shijian_a
                if len(shijian_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'

    #楼讯
    def get_news_title(self,response):
        try:
            news_title = response.xpath('//h1/text()').extract()
            for i in news_title:
                if len(i):
                    news_title = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    news_title = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(news_title))).strip().replace(' ', '')
                else:
                    news_title = 'NULL'
                return news_title
            if len(news_title) == 0:
                return 'NULL'
        except:
            return 'NULL'
    def get_news_pubtime(self,response):
        try:
            news_pubtime = response.xpath('//div[@class="title-bar"]/span/text()').extract()
            for i in news_pubtime:
                if len(i):
                    news_pubtime = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                    news_pubtime = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(news_pubtime))).strip().replace(' ', '')
                else:
                    news_pubtime = 'NULL'
                return news_pubtime
            if len(news_pubtime) == 0:
                news_pubtime_a = response.xpath('//div[@class="title_ext"]/span/text()').extract()
                for i in news_pubtime_a:
                    if len(i):
                        news_pubtime_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(i))).strip().replace(' ', '')
                        news_pubtime_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;', '', str(news_pubtime_a))).strip().replace(' ','')
                    else:
                        news_pubtime_a = 'NULL'
                    return news_pubtime_a
                if len(news_pubtime_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
    def get_news_content(self,response):
        try:
            news_content = re.compile('<div class="lp2">(.*?)<div class=', re.S).findall(response.text)
            for i in news_content:
                if len(i):
                    news_content = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;|&mdash;|\r|\t|&rdquo;|&ldquo;', '', str(i))).strip().replace(' ', '')
                    news_content = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;|&mdash;|\r|\t|&rdquo;|&ldquo;', '', str(news_content))).strip().replace(' ', '')
                else:
                    news_content = 'NULL'
                return news_content
            if len(news_content) == 0:
                news_content_a = re.compile('<div class="info">(.*?)<div class="copyright">', re.S).findall(response.text)
                for i in news_content_a:
                    if len(i):
                        news_content_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;|&mdash;|\r|\t|&rdquo;|&ldquo;', '', str(i))).strip().replace(' ', '')
                        news_content_a = str(re.sub('<.*?>|\\n|{1，7}|&nbsp;|&mdash;|\r|\t|&rdquo;|&ldquo;', '', str(news_content_a))).strip().replace(' ', '')
                    else:
                        news_content_a = 'NULL'
                    return news_content_a
                if len(news_content_a) == 0:
                    return 'NULL'
        except:
            return 'NULL'
