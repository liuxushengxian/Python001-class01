import scrapy
from scrapy.selector import Selector
from spiders.items import SpidersItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        # pass
        try:
            movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
            for movie in movies[:10]:
                item = SpidersItem()
                title = movie.xpath('./div[1]/@title')
                cate = movie.xpath('./div[2]/text()')
                time = movie.xpath('./div[4]/text()')

                item['title'] = title.extract_first().strip()
                item['cate'] = cate.extract()[1].strip()
                item['time'] = time.extract()[1].strip()
                
                #print(title.extract_first().strip())
                #print(cate.extract()[1].strip())
                #print(time.extract()[1].strip())
                
                yield item
        except:
            print('')
