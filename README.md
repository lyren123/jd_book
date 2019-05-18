# jd_book
crawl book information in jd.com

通过scrapy_redis分布式爬取京东图书所有相关商品信息

1:如果想开启运行分布式,多台服务器爬取数据,在seetings文件中将REDIS_URL地址更改为同一网段的ip

2:直接运行run.py文件即可开启爬虫, 会在控制台输出商品信息方便直观查看爬取进度

环境：scrapy框架+mongodb数据存储+scrapy_redis组件，运行爬虫所需要的python库和依赖在requirement.txt文件中
