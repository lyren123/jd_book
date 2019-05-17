# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
import json
from ..items import JdbookItem
class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['jd.com']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # 分组
        dt_list =response.xpath("//div[@class='mc']/dl/dt")
        # 获取图书的大分类
        for dt in dt_list:
            item = JdbookItem()
            item["cate"] = dt.xpath("./a/text()").extract_first()
            dd_list = dt.xpath("./following-sibling::dd[1]/em")
            for dd in dd_list:
                item["s_cate"] = dd.xpath("./a/text()").extract_first()
                item["cate_href"] = dd.xpath("./a/@href").extract_first()
                cate_url = "https:"+str(item["cate_href"])
                yield scrapy.Request(cate_url,meta={"item":deepcopy(item)},callback=self.parse_book)


    def parse_book(self,response):
        item = response.meta["item"]
        li_list = response.xpath("//ul[@class='gl-warp clearfix']/li")
        for li in li_list:
            item["book_href"] = li.xpath("./div/div[@class='p-name']/a/@href").extract_first()
            book_url = "https:"+str(item["book_href"])
            yield scrapy.Request(book_url,meta={"item":deepcopy(item)},callback=self.parse_detail)

    def parse_detail(self,response):
        # 在分类的详情页中获取关于每本书的详细信息
        item = response.meta["item"]
        item["book_name"] = response.xpath("//div[@id='name']/div[1]/text()").extract_first()
        item["press"] = response.xpath("//ul[@id='parameter2']/li[1]/a/text()").extract_first()
        item["publish_date"] = response.xpath("//ul[@id='parameter2']/li[contains(text(),'出版时间')]/text()").extract_first()
        # 商品价格有js生成,经过网页分析得知 "https://p.3.cn/prices/mgets?type=1&area=1_72_4137_0&pdtk=&pduid=1524592686&pdpin=&pdbp=0&skuIds=J_12090377&ext=11100000"

        # 利用正则表达式获取当前商品信息的sku
        num = re.findall(r"/(\d+).html",response.url)[0]
        price_url = "https://p.3.cn/prices/mgets?type=1&area=1_72_4137_0&pdtk=&pduid=1524592686&pdpin=&pdbp=0&skuIds=J_{}&ext=11100000".format(num)
        # print(222)
        yield scrapy.Request(price_url,meta={"item":deepcopy(item)},callback=self.parse_price,dont_filter=True)

    # 提取商品的价格
    def parse_price(self,response):
        item = response.meta["item"]
        price = json.loads(response.body.decode("gbk"))
        item["price"] = price[0]["p"]
        yield item

