学习笔记

## 开发环境配置

Pythong常见的Web框架：web.py，Django，Flask，Tornado，AIOHTTP，FastAPI，它们都遵循了MVC设计模式。

Django特点：Django是一个开放源代码的Web应用框架，是用python实现的。

设计模式是前人根据开发的经验，总结出的一套编程思想，依据此指导思想开发出框架、应用程序等。

#### MTV框架模式

模型（Model）、模板（Template）、视图（Views）

#### Django的版本

Django目前最新的是3.0版本，目前使用较多的是2.2.13（LTS），LTS表示会对这个版本做长期支持，业界已证实2.2.13版本是比较稳定的

```python
$ pip install django==2.2.13	# 升级低版本django: pip install --upgrade django==2.2.13
>>> import django
>>> django.__version__
'2.2.13'
```

## 创建项目和目录结构

#### Django和其他包的启动有区别

* 其他包导入后直接运行即可，Django需要配置MTV；
* 其他包运行一次就结束了，Django是以Web服务器的形式一直运行着；

#### Django启动分三步

1. 创建Django的项目；
2. 创建应用程序；
3. 真正的启动；

#### 创建Django项目

```python
$ django-admin startproject MyDjango	# MyDjango是项目名称

# 目录结构如下：
$ find MyDjango/
MyDjango/
MyDjango/manage.py		# manage.py是命令行工具，用于整个项目的管理
MyDjango/MyDjango
MyDjango/MyDjango/__init__.py
MyDjango/MyDjango/settings.py	# settings.py是项目的配置文件，例如数据库、支持的应用程序等
MyDjango/MyDjango/urls.py
MyDjango/MyDjango/wsgi.py
```

#### 创建Django应用程序（利用manage.py）

```python
$ python manage.py help 	# 查看该工具的具体功能
$ python manage.py startapp index 	# index是应用程序名称
index/migrations 	# 数据库迁移文件夹
index/models.py 	# 模型
index/apps.py 		# 当前app配置文件
index/admin.py 		# 管理后台
index/tests.py 		# 自动化测试
index/views.py 		# 视图
```

项目和应用程序之间通过urls.py关联起来

#### 启动和停止Django应用程序

```python
# 运行命令，默认是127.0.0.1:8000
$ python manage.py runserver
# 运行后，会读取默认的MyDjango.settings

$ python manage.py runserver 0.0.0.0:80
    
# 停止server使用CTRL+C
```

## 解析settings.py主要配置文件

```python
# 项目路径：python中常用的获取相对路径的方法，一定要记住
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 密钥：可以自行修改，主要用于生产环境的部署，防止外部跨站入侵
SECRET_KEY = 'p*d7^ue2xmk+1d(5!jk_1^lk2r1jf%!+@)k3!)hjo3(c%mygsu'
# 调试模式：会有大量的调试日志，不能用于生产环境。生产环境下要用wsgi
DEBUG = True
# 域名访问权限
ALLOWED_HOSTS = []
# App列表：Django默认支持的应用，从上到下依次加载，因此默认的不要随意修改次序，自己的应用添加在后面即可
INSTALLED_APPS = [
    ####  内置的后台管理系统
    'django.contrib.admin',
    ####  内置的用户认证系统
    'django.contrib.auth',
    #### 所有model元数据
    'django.contrib.contenttypes',
    #### 会话，表示当前访问网站的用户身份
    'django.contrib.sessions',
    #### 消息提示
    'django.contrib.messages',
    #### 静态资源路径
    'django.contrib.staticfiles',
    #### 注册自己的APP
    'index',
]
# 中间件是request和response对象之间的钩子：也有顺序问题，不要随意调整
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# url匹配，url的入口
ROOT_URLCONF = 'MyDjango.urls'
# 模板设置
TEMPLATES = [
    {
        #### 定义模板引擎
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #### 设置模板路径
        'DIRS': [],
        #### 是否在App里查找模板文件
        'APP_DIRS': True,
        #### 用于RequestContext上下文的调用函数
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# 
WSGI_APPLICATION = 'MyDjango.wsgi.application'
# 数据库配置，默认是sqlite，Django2.2使用mysqlclient或pymysql模块连接MySQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# export PATH=$PATH:/usr/local/mysql/bin
# OSError: mysql_config not found
# pip install mysqlclient
# pip install pymysql 这个常用，需要注意版本匹配
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'rootroot',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
    # 生产环境有可能连接第二个数据库
    # 'db2': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'mydatabase',
    #     'USER': 'mydatabaseuser',
    #     'PASSWORD': 'mypassword',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3307',
    # }
}
# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 静态文件 (CSS, JavaScript, Images)
STATIC_URL = '/static/'
```

总结：需要修改的部分主要有两部分，一是注册自己的app，二是数据库配置

## urls调度器

urls调度器接收用户的URL请求信息。

MyDjango/urls.py文件中的urlpatterns列表实现了从URL路由到视图（views）的映射功能，在此过程中它使用了一个Python模块，\*\*URLconf\*\*(URL configuration)，通常这个用于配置URL，所以调度器也叫做URLconf。

#### Django如何处理一个请求

当一个用户请求（浏览器发起的http请求，scrapy封装的http请求等等）Django站点的一个页面：

1. HttpRequest对象在进入urls调度器之前，Django中间件会为这个对象增加urlconf这样一个属性，HttpRequest对象拥有urlconf属性后，它的值将被用来替换ROOT_URLCONF设置；
2. Django加载URLconf模块并寻找可用的urlpatterns，Django依次匹配每个URL模式（字符串匹配和正则匹配）；
3. 一旦有URL匹配成功，Django导入并调用相关的视图，视图会获得如下参数：
   * 一个HttpRequest实例；
   * 一个或多个位置参数提供；

4. 如果没有URL匹配，或者匹配出现异常，Django会调用一个适当的错误处理视图。

#### 增加项目urls（项目MyDjango下的urls.py文件）

```python
from django.contrib import admin
from django.urls import path, include

# urlpatterns是固定名称，不可修改
urlpatterns = [
    path('admin/', admin.site.urls), 	# 第一个参数是请求的URL的解析，这里就是“请求的路径+admin”
    path('',include('index.urls')), 	# include导入应用程序，推荐使用这种方式。index就是前面startapp创建的应用。这里include后，就是要到index.urls中继续去寻找url和视图的匹配。
]
```

#### 增加index的urls

```python
from django.urls import path
from . import views 	# .表示当前文件所在目录

urlpatterns = [
    path('', views.index) 	# 去寻找view文件下的index函数
]
```

```python
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello Django!")
```

## 模块和包

* 模块：以.py结尾的Python程序，可以通过`python 程序名`直接运行。模块如果既需要被导入有需要被执行，可以通过`if __name__ == '__main__':`来做导入和执行的分隔；
* 包：存放多个模块的目录，\_\_init\_\_.py是包运行的初始化文件，可以是空文件；

#### 常见的导入方式

```python
import
from ... import ...
from ... import ... as ...

from . import Module1 	# import默认从python的site-package去导入，这里使用'.'表示当前文件所在目录
from .Pkg2 import M2 	# .Pkg2表示导入当前目录下的包Pkg2中的模块M2
```

## 让URL支持变量，URL正则，自定义过滤器

#### 带变量的URL

Django支持对URL设置变量，URL变量类型包括：

* str：字符串；
* int：整数；`path('<int:year>', views.myyear),`
* slug：备注；
* uuid：唯一的一串ID；
* path：路径

```python
# urls.py 文件
from django.urls import path, re_path, register_converter
from . import views, converters

# converters是我们自己写的文件，里面实现IntConverter类和FourDigitYearConverter类，类中要实现过滤规则（正则表达式），to_python，to_url。
register_converter(converters.IntConverter, 'myint') 	# 注册成自己的类型
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    # 带变量的URL
    path('<int:year>', views.year), 	# 只接收整数，其他类型返回404。接收后由views.py中的year函数处理（参考下一段代码）
	path('<int:year>/<str:name>', views.name), 	# 2020/abcdefg，多个参数传给name
    
    # 正则匹配，'?P'是关键字，固定写法。name是指传入变量的名字，后面Templates要用
    re_path('(?P<year>[0-9]{4}).html', views.myyear, name='urlyear'),

	# 自定义过滤器
	path('<myint:year>', views.year), 
    #path('<yyyy:year>', views.year), 
    
    # 以上有多个year，从上到下的顺序匹配
]
```

```python
# views.py 文件
from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello Django!")

# path('<int:year>', views.year), 
def year(request, year): 	# 第一个参数必须是request对象
    # return HttpResponse(year)
    return redirect('/2020.html')

# path('<int:year>/<str:name>', views.name),
def name(request, **kwargs): 	# 处理多个参数
    return HttpResponse(kwargs['name'])

# path('<myint:year>', views.year), 
# re_path('(?P<year>[0-9]{4}).html', views.myyear, name='urlyear'),
def myyear(request, year):
    return render(request, 'yearview.html')
# Templates文件夹中增加yearview.html文件：
# <div><a href="{% url 'urlyear' 2020 %}">2020 booklist</a></div>
```

## view视图快捷方式

对URL的处理就是把URL链接和view视图绑定。处理完成后返回的方式有两种：

* Response：正常的返回
* Render：对Response进一步封装

| 相应类型                                 | 说明                                        |
| ---------------------------------------- | ------------------------------------------- |
| HttpResponse('Hello World')              | HTTP状态码200，请求已成功被服务器接收       |
| HttpResponseRedirect('/admin/')          | HTTP状态码302，重定向Admin站点的URL         |
| HttpResponsePermanentRedirect('/admin/') | HTTP状态码301，永久重定向Admin站点的URL     |
| HttpResponseBadRequest('BadRequest')     | HTTP状态码400，访问的页面不存在或者请求错误 |
| HttpResponseNotFound('NotFound')         | HTTP状态码404，页面不存在或者网页的URL失效  |
| HttpResponseForbidden('NotFound')        | HTTP状态码403，没有访问权限                 |
| HttpResponseNotAllowed('NotAllowedGet')  | HTTP状态码405，不允许使用该请求方式         |
| HttpResponseSeverError('SeverError')     | HTTP状态码500，服务器内容错误               |

#### Django快捷函数

对常用的返回进行二次封装，常用的快捷函数有：

* render()：将给定的模板与给定的上下文字典组合在一起，并以渲染的文本返回一个HttpResponse对象；
* redirect()：将一个HttpResponseRedirect返回到传递的参数的适当URL；
* get_object_or_404()：在给定的模型管理器（model manager）上调用get()，但它会引发Http404而不是模型的DoesNotExist异常；

```python
def myyear(request, year):
    return render(request, 'yearview.html') 	# 将返回内容和文件yearview.html绑定，yearview.html需要手动创建

def year(request, year):
    return redirect('/2020.html') 	# 重新解析2020.html这个URL，常用于用户名密码后的跳转
```

## 使用ORM创建数据表

Model主要是做数据的增删改查。之前学习的PyMySQL，可以使用连接并且进行一个Query的查询，直接做SQL化的操作。Django并不直接操作数据库，它做了一个对象的提取，类名就是表名，类中的属性变成了表的字段。Django的ORM还自带了API，去操作数据库。

#### 模型和数据库

* 每个模型都是一个Python的类，这些类继承django.db.models.Model
* 模型类的每个属性都相当于一个数据库的字段
* Django提供了一个自动生成访问数据库的API

```python
from django.db import models
class Person(models.Model):
    # id = models.IntegerField(primary_key=True) 	# Django会自动创建，并设置为主键
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
# 上面类对应的SQL
CREATE TABLE myapp_preson(
	"id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL, 
    "last_name" varchar(30) NOT NULL, 
);

# 利用ORM设计表，ORM转为SQL的命令：
$ python manage.py makemigrations 	# ORM定义的类转为中间Python脚本（0001_auto_20200801.py）
$ python manage.py migrate 			# 中间Python脚本转为SQL的表
```

#### 问题1：提示找不到MySQL的配置文件

出错信息：django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'

实际上是Django找不到MySQL客户端。解决方法是在项目MyDiango的\_\_init\_\_.py中增加MySQL的安装。

```python
# pip install pymysql(如果没有pymysql，先要安装)
# Django默认使用的是MySQLdb，现在不适合于Python3.7版本，也不适合于Django2.2版本，所以这里要pymysql替换MySQLdb
import pymysql
pymysql.install_as_MySQLdb()

# 到这里可能还是找不到MySQL，需要增加系统路径
$ export PATH=$PATH:/usr/local/mysql/bin 	# 利用which mysql命令找到mysql路径，加入PATH
```

#### 问题2：提示版本不匹配

Django判断的是其默认的MySQLdb的版本，我们用pymysql替换后，将判断版本的语句删除即可。

```python
version = Database.version_info
#if version < (1, 3, 13):
#	raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```

#### 问题3：生成MySQL对应的表时，提示'str'没有'decode'属性

出错信息：AttributeError: 'str' object has no attribute 'decode'

这是python早期版本遗留的问题，是要通过decode和encode设置对应的一些字符编码。python3下不需要这种转换，出现这个错误之后可以根据错误提示找到文件位置，打开 operations.py 文件，找到以下代码，注释掉转换的代码即可。

```python
def last_executed_query(self, cursor, sql, params):
    query = getattr(cursor, '_executed', None)
    # if query is not None:
    #     query = query.decode(errors='replace')
	return query
```

## ORM API

ORM中的数据类型和SQL中的数据类型如何对应？？？要在Django的官方文档去看（注意版本为2.2），模型层->模型->字段类型->field types。需要我们掌握的类型有：

* AutoField
* CharField
* DateField, DateTimeField
* FloatField
* IntegerField

Django提供了一个shell，通过manage.py可以启动这个shell，在shell中可以验证ORM的API。

```python
# 找到manage.py所在目录，启动shell，进入交互模式
$ python manage.py shell
>>> from index.models import *

# 使用ORM框架api实现
# 增
>>> Name.objects.create(name='红楼梦', author='曹雪芹', stars='9.6')
>>> Name.objects.create(name='活着', author='余华', stars='9.4')

# 查
>>> Name.objects.get(id=2).name

# 改
>>> Name.objects.filter(name='红楼梦').update(name='石头记')

# 删单条数据
>>> Name.objects.filter(name='红楼梦').delete()
# 删全部数据
>>> Name.objects.all().delete()
```

## Django模板开发

* 模板变量：`{{variables}}`
* 从URL获取模板变量：`{% url 'urlyear'2020 %}`
* 读取静态资源内容：`{% static "css/header.css" %}`
* for遍历标签：`{% for type in type_list %}{% endfor %}`
* if判断标签：`{% if name.type==type.type %}{% endif %}`

#### 参考说明

**获取课程源码操作方法：**

切换分支：git checkout 5d

## 展示数据库中的内容

总结上面的流程：

1. 接收到URL后（books），先到项目的urls.py中去匹配urlpatterns，有可能会跳到应用的urls.py继续匹配；
2. 匹配后找到应用的views.py，请求（携带着url对应的conf）被传给views.py中的books函数，该函数使用ORM的API去获取数据库内容；
3. Name是在models.py定义的类（对应表），获取完后，books返回内容和templates下的bookslist.html页面绑定，最终返回给用户

## 豆瓣页面展示功能的需求分析

前面的课程学习了爬虫做数据的采集，用数据库做存储，然后用Pandas做数据的清洗，接下来就是做数据的展示了。利用template传递变量，展示的界面不太美观，所以Django做展示时一般都要去结合一些前端的框架。

Bootstrap Admin管理模板。

view视图通过model去获取要展示的数据。model是数据的模型。template结合前端的框架做展示。利用URLconf对URL进行处理（即urlpatterns）。

## urlconf与models配置

#### URLconf的处理

* http://ip/xxx
* http://ip/yyy
* http://ip/douban/xxx 
* http://ip/douban/yyy

如果功能简单，只用一个APP即可；如果相对douban做细致开发，将URL中的douban/注册成一个独立的APP。

```python
$ python manage.py startapp Douban 	# 注册新的APP，名字为Douban

# 在MyDjango下的settings.py中的INSTALLED_APPS列表最后增加'Douban'

# 在MyDjango下的urls.py中的urlpatterns列表增加对'Douban'的处理
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('index.urls')),
    path('douban/',include('Douban.urls')), 	# 路径'douban/'中的斜杠一定不能少，否则Django路径拼接会出错。前面不能加斜杠
]
```

http://ip:port/douban/index就指向了Douban.urls：

```python
from django.urls import path
from . import views 	# 当前目录（即当前APP下的views）

urlpatterns = [
    path('index', views.books_short),
]
```

Douban下的views.py：

```python
from django.shortcuts import render

# Create your views here.
from .models import T1
from django.db.models import Avg

def books_short(request):
    ###  从models取数据传给template  ###
    shorts = T1.objects.all()
    # 评论数量
    counter = T1.objects.all().count()

    # 平均星级
    # star_value = T1.objects.values('n_star')
    star_avg =f" {T1.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f} "
    # 情感倾向
    sent_avg =f" {T1.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f} "

    # 正向数量
    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5}
    plus = queryset.filter(**condtions).count()

    # 负向数量
    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()

    # return render(request, 'douban.html', locals())
    return render(request, 'result.html', locals())
```

如果是原生的Django项目，我们可以通过ORM编写类和属性，创建对应的表和字段。而实际工作中的场景是已经有现成的数据库，Django只需要展示其数据即可，那么可以通过命令将现有的表和字段反向导入成ORM的类和属性。

```python
$ python manage.py inspectdb > models.py 	# 将现有的数据库反向导入为ORM的类和属性，并保存为models.py
# inspectdb要导入的表是在settings.py中的DATABASES指定的数据库

# models.py 内容
from django.db import models

class T1(models.Model):
    id = models.BigAutoField(primary_key=True)
    n_star = models.IntegerField()
    short = models.CharField(max_length=400)
    sentiment = models.FloatField()

    # Meta表示元数据，不属于任何一个字段的数据。因为这个类是从已有的表反向导入的，会多一些额外信息。
    class Meta:
        managed = False		# 表示不能用migrate正向导出成SQL表 
        db_table = 't1'		# 原表的表名。默认的为Douban_T1
```

## views视图的编写

```python
from django.shortcuts import render

# Create your views here.
from .models import T1 	# T1就是通过SQL反向导入生成的模型
from django.db.models import Avg

def books_short(request):
    ###  从models取数据传给template  ###
    shorts = T1.objects.all()
    # 评论数量
    counter = T1.objects.all().count()

    # 平均星级，要用到聚合功能，返回的是QuerySet，其实就是字典
    # star_value = T1.objects.values('n_star')
    star_avg =f" {T1.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f} "
    # 情感倾向
    sent_avg =f" {T1.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f} "

    # 正向数量
    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5} 	# sentiment:字段名称；gte:大于等于；两者用__连接，字典格式，因为filter要求的参数是**kwargs
    plus = queryset.filter(**condtions).count()

    # 负向数量
    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()

    # return render(request, 'douban.html', locals())
    return render(request, 'result.html', locals())
```

Django的官方文档去看（注意版本为2.2），模型层->QuerySet->执行查询。Managers只能通过模型类访问。

检索全部对象：`T1.objects.all()`

聚合功能要参考模型层->高级->聚合。

## 结合bootstrap模板进行开发

上面views可以使用model产生的数据了，现在就要在view中把数据传递给template模板，为了更好的显示数据，引入一个叫做bootstrap的前端框架。

templates文件夹下放置了html文件；static文件夹下放置了css，fonts，images，js四个文件夹。css下的bootstrap.min.css文件，js下的bootstrap.min.js和jquery.js是bootstrap框架必不可少的三个文件。

bootstrap官方网站有很多实现好的，我们找一个符合我们要求的：startbootstrap.com/themes/sb-admin-2/。在这个网页上我们点击"view on GitHub"可以下载源代码，把css，fonts，images，js放到static中，html放到templates中。

栅格系统：把屏幕宽度分成十二格，根据屏幕宽度自动调整组件尺寸。

`{% extends "base_layout.html" %}` 把其他页面继承过来

`{% load static %}` 加载static，意味着后面可以使用`{% static ... %}`

views已经通过locals把获取的数据传递给templates，templates可以直接使用。

饼图的数据是通过js代码去提取的。

## 如何阅读Django的源代码

manage.py直接定义了main函数，这里可以作为程序的入口。

`python manage.py runserver 8080` ，根据runserver进一步跟踪和学习，ruanserver会实例化WSGIserver，动态创建一些类等等。

