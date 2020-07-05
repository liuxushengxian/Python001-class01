# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

dbInfo = {
    'host' : 'localhost', 		# 主机或url
    'port' : '3306', 			# 端口
    'user' : 'root', 			# 用户名
    'password' : 'rootroot', 	# 密码
    'db' : 'test', 			    # 数据库名
    'table' : 'maoyan',         # 表名
}

class SpidersPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host = self.host, 
            port = self.port, 
            user = self.user, 
            password = self.password, 
            db = self.db)

    def __init__(self, dbInfo): 
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.table = dbInfo['table']

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        sql = 'INSERT INTO {table} (`{fields}`) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE {update}'.format(
                table = self.table,
                fields = '`,`'.join(item_dict.keys()),
                update = ','.join(['`{field}`=VALUES(`{field}`)'.format(field=field) for field in item_dict.keys()])
            )
        cur = self.conn.cursor()
        try:
            cur.execute(sql, item_dict.values())
        except:
            self.conn.rollback()
            print('save to db failed')
        finally:
            cur.close()

        return item

    def close_spider(self, spider):
        self.conn.close()