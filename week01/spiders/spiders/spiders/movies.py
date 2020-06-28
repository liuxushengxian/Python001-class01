# -*- coding: utf-8 -*-
import scrapy
from spiders.items import SpidersItem
# from bs4 import BeautifulSoup
from scrapy.selector import Selector


class MoviesSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'movies'
    allowed_domains = ['maoyan.com']
    # 起始URL列表
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        #print('*******************************')
        #print(response.text)
        #print('*******************************')

        item = SpidersItem()
        
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for movie in movies[:10]:
            title = movie.xpath('./div/span[@class="name "]/text()')
            cate = movie.xpath('./div[2]/text()')
            time = movie.xpath('./div[4]/text()')

            item['title'] = title.extract()
            item['cate'] = cate.extract()[0].strip()
            item['time'] = time.extract()[0].strip()

            
            print(title.extract())
            print(cate.extract()[0].strip())
            print(time.extract()[0].strip())
            
        yield item
