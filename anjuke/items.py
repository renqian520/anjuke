# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedisItem(scrapy.Item):
    url = scrapy.Field()
#楼盘首页
class Mongodb_detail_Item(scrapy.Item):
    url = scrapy.Field() #楼盘首页url  https://hz.fang.anjuke.com/loupan/252380.html?from=AF_RANK_1
    url_pid = scrapy.Field() #关联的id
    img = scrapy.Field() #图片
    leimu = scrapy.Field() #杭州安居客 > 杭州楼盘 > 江干楼盘 > 市中心楼盘 > 绿地华家池印

#楼盘详情
class Mongodb_canshu_Item(scrapy.Item):
    url = scrapy.Field() # https://hz.fang.anjuke.com/loupan/canshu-252689.html
    url_pid = scrapy.Field()  # 关联的id
    name = scrapy.Field() #楼盘名称 绿地华家池印
    tedian = scrapy.Field() #楼盘特点 轨交房 投资地产 商场 银行 精装修
    singleprice =  scrapy.Field() # 住宅 52000 元/㎡
    allprice = scrapy.Field() # 参考价格住宅 1408万元/套起
    leixing = scrapy.Field()  # 物业类型 住宅
    developers = scrapy.Field() # 开发商 绿地控股集团（浙江）房地产开发有限公司
    quyu = scrapy.Field() # 区域位置 江干- 市中心
    dizhi = scrapy.Field()  # 楼盘地址 秋涛北路217号
    dianhua = scrapy.Field()  # 售楼处电话 400 056 1382
    shoufu = scrapy.Field() #最低首付 住宅 422.4 万（首付比例：30%）
    yuegong = scrapy.Field() #月供 住宅 52308.43元 （按最低首付，20年等额本息）
    huxing = scrapy.Field() # 楼盘户型 3室户型 (1)， 4室户型 (3)
    kaipan = scrapy.Field() # 最新开盘 待定
    shijian = scrapy.Field() # 交房时间 2018年06月30日
    shouloudizhi = scrapy.Field() #售楼处地址 江干区秋涛北路217号
    xukezheng = scrapy.Field() #预售许可证 杭售许字(2015)第000052号；杭售许字(2015)第000086号；杭售许字(2016)第000069号；
    jianzuleixing = scrapy.Field() # 建筑类型 高层
    nianxian = scrapy.Field() # 产权年限 住宅：70年
    rongji = scrapy.Field() # 容积率 住宅：3.2
    lvhua = scrapy.Field() #绿化率 30%
    hushu = scrapy.Field() # 规划户数 953户
    louceng = scrapy.Field() #楼层状况 高层、多层
    guanli = scrapy.Field() #物业管理费 住宅：5元/m²/月
    wuye = scrapy.Field() #物业公司 上海绿地物业服务有限公司
    chewei = scrapy.Field() #车位数 1285
    cheweibi = scrapy.Field() # 车位比1:1.2

#用户点评
class Mongodb_dianping_Item(scrapy.Item):
    url = scrapy.Field() # https://hz.fang.anjuke.com/loupan/dianping-410192.htmls/?from=loupan_tab
    url_pid = scrapy.Field()  # 关联的id
    content = scrapy.Field() #点评内容 这个楼盘的名字真是，距离钱塘江和西湖都很远，就旁边有个北塘河吧，不知道为什么叫这个名字，这开发商很少用这么诗意的名字，不过听听是挺美的
    pubtime = scrapy.Field() # 发布时间 2016-10-22
    author = scrapy.Field() # 迪先生

#动态资讯
class Mongodb_officialnews_Item(scrapy.Item):
    url = scrapy.Field() #https://hz.fang.anjuke.com/loupan/officialnews-252168.html?
    url_pid = scrapy.Field() # 关联的id
    news_url = scrapy.Field() # https://hz.fang.anjuke.com/dongtai/2017-12-12/1331092.html
    title = scrapy.Field() # 绿都南江壹号在售230-480㎡户型
    pubtime = scrapy.Field() # 2017年12月12日 15:07
    content = scrapy.Field() # 2017年12月12日讯：绿都南江壹号位于萧山主城区高桥路与晨晖路口南面

#楼盘房源
class Mongodb_fangyuan_Item(scrapy.Item):
    url = scrapy.Field() # 房源url https://hz.fang.anjuke.com/fangyuan/9616030.html
    url_pid = scrapy.Field()  # 关联的id
    fang_title = scrapy.Field() # 金城路上，滨水墅境，融信永兴首府全城争藏
    fang_shoujia = scrapy.Field() # 售价待定
    fang_fangxing = scrapy.Field() #房型4室2厅2卫
    fang_youhui = scrapy.Field() # 优惠暂无优惠
    fang_mianji = scrapy.Field() #面积126.00平米
    fang_shoufu = scrapy.Field() #参考首付105万
    fang_chaoxiang = scrapy.Field() #朝向南
    fang_yuegong = scrapy.Field() #参考月供 12966元
    fang_louceng = scrapy.Field() #楼层12/25（27号楼）
    fang_leixing = scrapy.Field() #物业类型住宅
    fang_zhuangxiu = scrapy.Field() #装修毛坯
    fang_dizhi = scrapy.Field() #地址[ 萧山 - 萧山新城 ] 新康路,近通广路
    fang_shijian = scrapy.Field() #交房时间待定

#楼讯
class Mongodb_news_Item(scrapy.Item):
    url = scrapy.Field() #https://hz.news.anjuke.com/market/405268.html?from=leading_toutiao_view
    news_title = scrapy.Field() #供需逆转，催生买房悲喜剧
    news_pubtime = scrapy.Field() #2017年12月28日 09:47
    news_content = scrapy.Field() # 2017年的新房市场，在大半年时间里都热浪滚滚。截至12月26日






