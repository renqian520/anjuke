# anjuke
安居客新房爬虫（Scrapy、Redis）

基于Python+scrapy+redis+mongodb的分布式爬虫实现框架

scrapy runspider anjukeredisurl.py  主要功能是抓取种子url，保存到redis

scrapy runspider anjukeredisnews.py 主要功能是抓取种子url，保存到redis

scrapy runspider anjukemongodburl.py  主要是从redis里面读url，解析数据保存到mongodb （拓展到其他机器,修改REDIS_HOST = "主机ip"，都是从redis里面读url,MONGODB_HOST = "存储服务器ip"）

middlewares.ProxyMiddleware  使用阿布云代理服务器轮换请求IP 


                                                 安居客新房楼盘首页信息mongodb图示
![安居客新房楼盘首页信息](https://github.com/renqian520/anjuke/blob/master/%E5%AE%89%E5%B1%85%E5%AE%A2%E6%96%B0%E6%88%BF%E6%A5%BC%E7%9B%98%E9%A6%96%E9%A1%B5%E4%BF%A1%E6%81%AF.jpg)                                             

                                                 安居客新房楼盘参数信息mongodb图示
![安居客新房楼盘参数信息](https://github.com/renqian520/anjuke/blob/master/%E5%AE%89%E5%B1%85%E5%AE%A2%E6%96%B0%E6%88%BF%E6%A5%BC%E7%9B%98%E5%8F%82%E6%95%B0%E4%BF%A1%E6%81%AF.jpg)

                                                 安居客新房楼盘房源信息mongodb图示
![安居客新房楼盘房源信息](https://github.com/renqian520/anjuke/blob/master/%E5%AE%89%E5%B1%85%E5%AE%A2%E6%96%B0%E6%88%BF%E6%A5%BC%E7%9B%98%E6%88%BF%E6%BA%90%E4%BF%A1%E6%81%AF.jpg)

                                                 安居客新房楼盘点评信息mongodb图示
![安居客新房楼盘点评信息](https://github.com/renqian520/anjuke/blob/master/%E5%AE%89%E5%B1%85%E5%AE%A2%E6%96%B0%E6%88%BF%E6%A5%BC%E7%9B%98%E7%82%B9%E8%AF%84%E4%BF%A1%E6%81%AF.jpg)

                                                 安居客新房楼盘楼讯信息mongodb图示
![安居客新房楼盘楼讯信息](https://github.com/renqian520/anjuke/blob/master/%E5%AE%89%E5%B1%85%E5%AE%A2%E6%96%B0%E6%88%BF%E6%A5%BC%E7%9B%98%E6%A5%BC%E8%AE%AF%E4%BF%A1%E6%81%AF.jpg)

                                                 安居客新房楼盘动态资讯信息mongodb图示
![安居客新房楼盘动态资讯信息](https://github.com/renqian520/anjuke/blob/master/%E5%AE%89%E5%B1%85%E5%AE%A2%E6%96%B0%E6%88%BF%E6%A5%BC%E7%9B%98%E5%8A%A8%E6%80%81%E8%B5%84%E8%AE%AF%E4%BF%A1%E6%81%AF.jpg)
