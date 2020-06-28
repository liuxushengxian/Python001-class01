# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SpidersPipeline:
    def process_item(self, item, spider):
        title = item['title']
        cate = item['cate']
        time = item['time']
        output = str(title) + ',' + str(cate) + ',' + str(time) + '\n'
        with open('maoyan_movie.csv', 'a+', encoding='utf-8') as result:
            result.write(output)
        return item
