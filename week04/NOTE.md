## pandas简介

pandas：python中的excel

sklearn：数据集（用于机器学习等）

```python
from sklearn import datasets 	# 引入数据集

iris = datasets.load_iris()		# 鸢尾花数据集
X, y = iris.data, iris.target	# iris是个字典，取出特征数据和分类结果

# iris.feature_names 查看特征名称
# iris.target_names 查看标签名称

# 按照3比1的比例划分训练集和测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# load_xxx 		各种数据集
# load_boston 	Boston房屋价格 回归
# load_digits 	手写体 分类
# load_iris 	鸢尾花 分类聚类
```

numpy：python中的数学库，用于数学分析

matplotlib：数据可视化

```python
import pandas as pd
import numpy as np
import matplotlib as plt
import os

pwd = os.path.dirname(os.path.realpath(__file__))	# 获取本文件的绝对路径
book = os.path.join(pwd,'book_utf8.csv')	# 获取文件名
# df = pd.read_csv('book_utf8.csv')		# 如果执行命令时所在路径有数据文件，则可以直接调用
df = pd.read_csv(book)		# df是DataFrame数据结构，可以理解为表格

# print(df) 直接打印全部内容			
# df['还行'] 筛选标题为"还行"这一列，df没有表头的情况下，默认将第一行数据作为表头
# df[0:3] 切片方式筛选，显示前3行
# df.columns = ['star', 'vote', 'shorts'] 增加列名（即表头）
# df.loc[1:3, ['star']] 显示特定的行、列
# df['star'] == '力荐' 返回结果为True/False
# df[ df['star'] == '力荐' ] 过滤数据
# df.dropna() 缺失数据的处理
# df.groupby('star').sum() 数据聚合，统计不同star的数目
# 创建新列
star_to_number = {
    '力荐' : 5,
    '推荐' : 4,
    '还行' : 3,
    '较差' : 2,
    '很差' : 1
}
# 利用map将star和number做映射，然后创建新列new_star
df['new_star'] = df['star'].map(star_to_number)
print(df)
```

## pandas基本数据类型

#### Series数据结构

Series可以当作Excel中的一行或一列，最好当作一列来看待，因为Series来自于numpy，numpy中认为Series是以列的形式去组成的。列中的元素称为value，每个value都有index。这个索引是Series自动添加的，而且这个索引是可以更改的。

#### DataFrame数据结构

Series可以当作Excel中的一个表格（由多行和多列组成）。行和列都有索引，也都可以更改。

```python
import pandas as pd
import numpy as np

# 从列表创建Series, 自动创建索引0，1，2...，dtype: object
pd.Series(['a', 'b', 'c'])t

# 通过字典创建带索引的Series
s1 = pd.Series({'a':11, 'b':22, 'c':33})

# 通过关键字创建带索引的Series
s2 = pd.Series([11, 22, 33], index = ['a', 'b', 'c'])

# 获取全部索引
s1.index
# 获取全部值
s1.values

# 类型
type(s1.values)    # <class 'numpy.ndarray'> 和下面使用np.array创建是一样的
type(np.array(['a', 'b']))

# 转换为列表
s1.values.tolist()

# 使用index会提升查询性能
#    如果index唯一，pandas会使用哈希表优化，查询性能为O(1)
#    如果index有序不唯一，pandas会使用二分查找算法，查询性能为O(logN)
#    如果index完全随机，每次查询都要扫全表，查询性能为O(N)


# 列表创建dataframe
df1 = pd.DataFrame(['a', 'b', 'c', 'd'])
# 嵌套列表创建dataframe
df2 = pd.DataFrame([
                     ['a', 'b'], 
                     ['c', 'd']
                    ])
# 自定义列索引（列标题）
df2.columns= ['one', 'two']
# 自定义行索引
df2.index = ['first', 'second']

# 可以在创建时直接指定 DataFrame([...] , columns='...', index='...' )
# 查看索引： df2.columns, df2.index
type(df2.values)	# <class 'numpy.ndarray'>
```

## pandas数据导入

pandas支持大量格式的导入，通过read_xxx()的方法。

```python
import pandas as pd

# 导入excel文件，需要pip install xlrd
excel1 = pd.read_excel(r'1.xlsx')
# 指定导入哪个Sheet
pd.read_excel(r'1.xlsx', sheet_name = 0)
# 对于空白的，pandas显示为Nan，pandas可以使用na相关的方法来处理空值

# 导入csv文件
pd.read_csv(r'c:\file.csv',sep=' ', nrow=10, encoding='utf-8')
# 导入txt文件
pd.read_table(r'file.txt', sep=' ')
# 导入sql
import pymysql
sql = 'SELECT * FROM mytable'
conn = pymysql.connect('ip','name','pass','dbname','charset=utf8')
df = pd.read_sql(sql, conn)

# 熟悉数据
# 显示前几行
excel1.head(3)
# 行列数量
excel1.shape
# 详细信息
excel1.info()
excel1.describe()
```

## pandas数据预处理

缺失值处理和重复值处理。

```python
import pandas as pd
import numpy as np

x = pd.Series([ 1, 2, np.nan, 3, 4, 5, 6, np.nan, 8])
# 检验序列中是否存在缺失值
x.hasnans		# 返回bool类型

# 如果是纯数字的，将缺失值填充为平均值
x.fillna(value = x.mean()) 	# 注意，原有的x是不变的，填充后返回的是新的变量

# 前向填充缺失值
df3 = pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
                 
df3.isnull().sum() 	# 查看缺失值汇总
df3.ffill() 		# 用上一行填充
df3.ffill(axis=1) 	# 用前一列填充
# 填充要根据数据的实际意义去做，比如如果数据代表的是人的性别，那就没法填充了，只能通过人工或者预测的手段

# 缺失值删除
df3.info()
df3.dropna() 	# 删除有缺失值的整行

# 填充缺失值
df3.fillna('无')

# 重复值处理
df3.drop_duplicates()
```

## pandas数据调整

```python
# 行列调整
df = pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
# 列的选择，多个列要用列表，一定不能使用元组
df1 = df[ ['A', 'C'] ]

# 列的选择也可以使用数字序号
df.iloc[:, [0,2]] # :表示所有行，获得第1和第3列

# 行选择
df.loc[ [0, 2] ] # 选择第1行和第3行
df.loc[ 0:2    ] # 选择第1行到第3行

# 比较
df[ ( df['A']<5 ) & ( df['C']<4 ) ]


# 数值替换

# 一对一替换
# 用于单个异常值处理，将4替换为40
df['C'].replace(4,40)

import numpy as np
df.replace(np.NaN, 0)

# 多对一替换
df.replace([4,5,8], 1000)

# 多对多替换
df.replace({4:400, 5:500, 8:800})


# 排序
# 按照指定列降序排列
df.sort_values ( by = ['A'] , ascending = False)

# 多列排序
df.sort_values ( by = ['A','C'] ,ascending = [True,False])


# 删除
# 删除列
df.drop( 'A' ,axis = 1)

# 删除行
df.drop( 3 ,axis = 0)

# 删除特定行，注意NaN对于判断也是成立的
df [  df['A'] < 4 ]


# 行列互换
df.T
df.T.T

# 索引重塑
df4 = pd.DataFrame([
                     ['a', 'b', 'c'], 
                     ['d', 'e', 'f']
                    ],
                    columns= ['one', 'two', 'three'],
                    index = ['first', 'second']
                   )       
df4.stack()		# 数据展开
df4.unstack() 	# 数据反向展开
df4.stack().reset_index()  	# 重置索引，可以把展开的透视表中空白的内容填充      
```

## pandas基本计算操作

pandas基本计算包括行与列之间的计算，列与列之间的计算，利用数学的参数去处理pandas数据。

```python
import pandas as pd
# python中的None和numpy中的NaN在pandas中是等价的
df = pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
# 算数运算
# 两列之间的加减乘除，NaN是无法参与运算的，结果仍然是NaN
df['A'] + df['C'] 

# 任意一列加/减一个常数值，这一列中的所有值都加/减这个常数值
df['A'] + 5

# 比较运算，空值的比较全为False
df['A'] > df ['C']  

# count非空值计数
df.count()

# 非空值每列求和
df.sum()
df['A'].sum()

# mean求均值，max求最大值，min求最小值，median求中位数，mode求众数，var求方差，std求标准差
# 其他的函数参考pandas的官方文档
```

## pandas分组聚合

```python
import pandas as pd
import numpy as np

# 分组，源数据是列表嵌套字典，这是工作中常见的
sales = [{'account': 'Jones LLC','type':'a', 'Jan': 150, 'Feb': 200, 'Mar': 140},
         {'account': 'Alpha Co','type':'b',  'Jan': 200, 'Feb': 210, 'Mar': 215},
         {'account': 'Blue Inc','type':'a',  'Jan': 50,  'Feb': 90,  'Mar': 95 }]

df2 = pd.DataFrame(sales)
df2.groupby('type').groups	# 分组后相当于把一个DataFrame分成多个DataFrame
# groupby('type')返回的是一个DataFrameGroupBy对象
for a, b in df2.groupby('type'):	# 我们知道要分为两组可以通过这种方式去取
    print(a)
    print(b)

# 分组后再计算
df2.groupby('type').count()
# df2.groupby('Jan').sum()

# 聚合，各类型产品的销售数量和销售总额，aggregate可简写为agg
df2.groupby('type').aggregate( {'type':'count' , 'Feb':'sum' })

group = ['x','y','z']
data = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "salary":np.random.randint(5,50,10),
    "age":np.random.randint(15,50,10)
    })

data.groupby('group').agg('mean')
data.groupby('group').mean().to_dict()
data.groupby('group').transform('mean')	# 不合并，计算mean结果

# 数据透视表（这个和excel中的一样）
pd.pivot_table(data, 
               values='salary', 
               columns='group', 
               index='age', 
               aggfunc='count', 
               margins=True  
            ).reset_index()
# groupby可以参考数据库中的groupby
```

## pandas多表拼接

pandas中的拼接只需要简单了解即可，用的不多。因为pandas的数据绝大部分来源于数据库，数据库提供数据时一般都会进行拼接。

```python
group = ['x','y','z']
data1 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "age":np.random.randint(15,50,10)
    })

data2 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "salary":np.random.randint(5,50,10),
    })

data3 = pd.DataFrame({
    "group":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "age":np.random.randint(15,50,10),
    "salary":np.random.randint(5,50,10),
    })

# 一对一，merge发现它们的公共列是group，利用group进行拼接
pd.merge(data1, data2)

# 多对一，如果有多个公共列，要指定公共列
pd.merge(data3, data2, on='group')

# 多对多，多个公共列自行匹配
pd.merge(data3, data2)

# 连接键类型，解决没有公共列问题
pd.merge(data3, data2, left_on= 'age', right_on='salary')

# 连接方式
# 内连接，不指明连接方式，默认都是内连接
pd.merge(data3, data2, on= 'group', how='inner')
# 左连接 left，右连接 right，外连接 outer

# 纵向拼接，工作中用到最多
pd.concat([data1, data2])
```

## pandas输出和绘图

两种输出：第一种是to_dict转为字典，第二种是保存为文件。

```python
# 导出为.xlsx文件
df.to_excel( excel_writer = r'file.xlsx')

# 设置Sheet名称
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1')

# 设置索引，设置参数index=False就可以在导出时把这种索引去掉
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1', index = False)

# 设置要导出的列
df.to_excel( excel_writer = r'file.xlsx', sheet_name = 'sheet1', 
             index = False, columns = ['col1','col2'])

# 设置编码格式，输出文件是在Linux或者Mac或者安卓上时，用utf-8；是在windows上时，用GBK
enconding = 'utf-8'

# 缺失值处理
na_rep = 0 # 缺失值填充为0

# 无穷值处理
inf_rep = 0

# 导出为.csv文件
to_csv()

# 性能
df.to_pickle('xx.pkl') 

agg(sum) # 快，尽量使用内置函数
agg(lambda x: x.sum()) # 慢
```

```python
dates = pd.date_range('20200101', periods=12)
df = pd.DataFrame(np.random.randn(12,4), index=dates, columns=list('ABCD'))

#                    A         B         C         D
# 2020-01-01  0.046485 -0.556209  1.062881 -1.174129
# 2020-01-02  1.066051 -0.343081  1.054913  1.601051
# 2020-01-03  0.191064 -0.386905  0.516403  0.259818
# 2020-01-04 -0.168462 -1.488041 -0.457658  0.913574
# 2020-01-05 -0.502614  1.235633 -0.578284 -0.362737
# 2020-01-06 -0.193310  0.652285 -0.346359  0.347364
# 2020-01-07  2.308562 -0.679108  0.856449  0.490840
# 2020-01-08  0.871489  0.338133 -0.163669  0.300147
# 2020-01-09 -1.245250  0.667357 -1.287782  1.494880
# 2020-01-10  0.387925 -1.058867 -0.397298  0.514921
# 2020-01-11 -0.440884  0.904307  1.338720  0.612919
# 2020-01-12 -0.864941 -0.358934 -0.203868 -1.191186

import matplotlib.pyplot as plt
plt.plot(df.index, df['A'], )	# 返回的是Line2D对象
plt.show()

plt.plot(df.index, df['A'], 
        color='#FFAA00',    # 颜色
        linestyle='--',     # 线条样式
        linewidth=3,        # 线条宽度
        marker='D')         # 点标记
plt.show()

# seaborn其实是在matplotlib的基础上进行了更高级的API封装，从而使绘图更容易、更美观
import seaborn as sns
# 绘制散点图
plt.scatter(df.index, df['A'])
plt.show()

# 美化plt
sns.set_style('darkgrid')
plt.scatter(df.index, df['A'])
plt.show()
```

## jieba分词与提取关键词

#### 分词

```python
import jieba
strings = ['我来自极客大学', 'Python进阶训练营真好玩']

for string in strings:
    result = jieba.cut(string, cut_all=False) 	# 精确模式
    print('Default Mode: ' + '/'.join(list(result)))

for string in strings:
    result = jieba.cut(string, cut_all=True) 	# 全模式，主要用于搜索引擎去搜索
    print('Full Mode: ' + '/'.join(list(result)))

result = jieba.cut('钟南山院士接受采访新冠不会二次暴发') 	# 默认是精确模式
print('/'.join(list(result)))
# "新冠" 没有在词典中，但是被Viterbi算法识别出来了

result = jieba.cut_for_search('小明硕士毕业于中国科学院计算所，后在日本京都大学深造') # 搜索引擎模式
print('Search Mode: ' + '/'.join(list(result)))
```

#### 提取关键词（结束词用于屏蔽）

```python
import jieba.analyse
text = '机器学习，需要一定的数学基础，需要掌握的数学基础知识特别多，如果从头到尾开始学，估计大部分人来不及，我建议先学习最基础的数学知识'
# 基于TF-IDF算法进行关键词抽取（常用）
tfidf = jieba.analyse.extract_tags(text,
topK=5,  				# 权重最大的topK个关键词
withWeight=True)        # 返回每个关键字的权重值
# 基于TextRank算法进行关键词抽取
textrank = jieba.analyse.textrank(text,
topK=5,                  # 权重最大的topK个关键词
withWeight=False)        # 返回每个关键字的权重值

import pprint            # pprint 模块提供了打印出任何Python数据结构的类和方法
pprint.pprint(tfidf)
pprint.pprint(textrank)

# 结束词是指在提取关键词时需要屏蔽的词
stop_words=r'2jieba/extra_dict/stop_words.txt'
# stop_words 的文件格式是文本文件，每行一个词语
jieba.analyse.set_stop_words(stop_words)

textrank = jieba.analyse.textrank(text,
topK=5,                   
withWeight=False)         
pprint.pprint(textrank)
```

#### 自定义用户词典

词典格式示例：极客大学Python进阶训练营 3 nt，分别为词名 权重 词性

```python
import jieba
string = '极客大学Python进阶训练营真好玩'
user_dict=r'2jieba/extra_dict/user_dict.txt'

# 自定义词典
jieba.load_userdict(user_dict)

result = jieba.cut(string, cut_all=False)
print('自定义: ' + '/'.join(list(result)))

print('=' * 40 )

# 动态添加词典
jieba.add_word('极客大学')

# 动态删除词典
jieba.del_word('自定义词')

result = jieba.cut(string, cut_all=False)
print('动态添加: ' + '/'.join(list(result)))

print('=' * 40 )

string2 = '我们中出了一个叛徒'
result = jieba.cut(string2, cut_all=False)
print('错误分词: ' + '/'.join(list(result)))

print('=' * 40 )
# 关闭自动计算词频
result = jieba.cut(string2, HMM=False)
print('关闭词频: ' + '/'.join(list(result)))

print('=' * 40 )
# 调整分词，合并
jieba.suggest_freq('中出', True)

result = jieba.cut(string2, HMM=False)
print('分词合并: ' + '/'.join(list(result)))

print('=' * 40 )
# 调整词频，分开分词
string3 = '如果放到Post中将出错'
jieba.suggest_freq(('中','将'), True)
result = jieba.cut(string3, HMM=False)
print('分开分词: ' + '/'.join(list(result)))
```

## SnowNLP情感倾向分析

```python
from snownlp import SnowNLP
text = '其实故事本来真的只值三星当初的中篇就足够了但是啊看到最后我又一次被东野叔的反战思想打动了所以就加多一星吧'
s = SnowNLP(text)

# 1 中文分词
s.words

# 2 词性标注 (隐马尔可夫模型)
list(s.tags)

# 3 情感分析（朴素贝叶斯分类器）（训练数据使用的是购物的数据，用于饭店评价、购物评价）
s.sentiments	# 结果是从0到1，越接近1，评价越正向

text2 = '这本书烂透了'
s2 = SnowNLP(text2)
s2.sentiments

# 4 拼音（Trie树）
s.pinyin

# 5 繁体转简体
text3 = '後面這些是繁體字'
s3 = SnowNLP(text3)
s3.han

# 6 提取关键字
s.keywords(limit=5)

# 7 信息衡量
s.tf # 词频越大越重要
s.idf # 包含此条的文档越少，n越小，idf越大，说明词条t越重要

# 8 训练
from snownlp import seg
seg.train('data.txt')
seg.save('seg.marshal')
# 修改snownlp/seg/__init__.py的 data_path 指向新的模型即可
```

```python
import pandas as pd
from snownlp import SnowNLP

# 加载爬虫的原始评论数据
df = pd.read_csv('book_utf8.csv')
# 调整格式
df.columns = ['star', 'vote', 'shorts']
star_to_number = {
    '力荐' : 5,
    '推荐' : 4,
    '还行' : 3,
    '较差' : 2,
    '很差' : 1
}
df['new_star'] = df['star'].map(star_to_number)
# 用第一个评论做测试
first_line = df[df['new_star'] == 3].iloc[0]
text = first_line['shorts']
s = SnowNLP(text)
print(f'情感倾向: {s.sentiments} , 文本内容: {text}')

# 封装一个情感分析的函数
def _sentiment(text):
    s = SnowNLP(text)
    return s.sentiments

df["sentiment"] = df.shorts.apply(_sentiment)
# 查看结果
df.head()
# 分析平均值
df.sentiment.mean() 


# 训练模型
# from snownlp import sentiment
# sentiment.train('neg.txt','pos.txt')
# sentiment.save('sentiment.marshal')

del df['star']
del df['vote']
order = ['new_star', 'shorts', 'sentiment']
df = df[order]
df.rename(columns={'new_star':'n_star','shorts':'short'},inplace=True) 
df.to_csv('result.csv', index=None)
```

pandas中map() 和apply() 的区别，对于初学者很容易产生迷惑

map()：针对pandas 中的DataFrame中列进行迭代操作

apply(): 针对pandas中DataFrame中行进行迭代操作
