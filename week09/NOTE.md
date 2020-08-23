学习笔记

### 1.Django源码分析之URLconf的偏函数

Django中最主要的最基本的代码有四个部分：

1. URLconf：处理用户请求路径，将路径转到对应View视图去处理；
2. View视图：关联Model模型，关联Template模板，View视图处理用户请求到用户返回的整个流程；
3. Template模板：匹配特殊符号，例如两个花括号括起来的就是变量；
4. Model模型：用到一个查询管理器，默认是object，自动创建主键。

Django下的urls.py文件：

```python
urlpatterns = [
    # path匹配标准的路径
    path('', views.index),
    # 正则匹配，'?P'是关键字，固定写法。name是指传入变量的名字，后面Templates要用
    re_path('(?P<year>[0-9]{4}).html', views.myyear, name='urlyear'),
]
```

从源码层面对比path()和re_path()。Ctrl+鼠标左键，点击path，跳转到path的定义处（Mac下是Command+鼠标左键）。可以看到里面有个partial，这是从functools导入的，作用是“冻结”部分参数使用固定值，只传递关键参数给_path

```python
# site-packages/django/urls/conf.py
path = partial(_path, Pattern=RoutePattern) 	# Pattern是关键字参数
re_path = partial(_path, Pattern=RegexPattern)

# 官方文档：https://docs.python.org/zh-cn/3.7/library/functools.html
# 下面是官方文档中partial的实现，
def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords): 	# 闭包的内部函数
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords) 	# 更新关键字参数
        return func(*args, *fargs, **newkeywords) 	# func必须是一个函数或者可调用对象
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

# 官方demo
from functools import partial
basetwo = partial(int, base=2) 	# 利用偏函数固定参数base为2，将int转二进制为十进制定义为新的函数basetwo
basetwo.__doc__ = 'Convert base 2 string to an int.' 	# 更新说明
basetwo('10010') 	# 18
```

注意事项：

1. partial 第一个参数必须是可调用对象
2. 参数传递顺序是从左到右，但不能超过原函数参数个数
3. 关键字参数会覆盖partial中定义好的参数

### 2.Django源码分析之URLconf的include

```python
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls), 	# 路径匹配view视图
    path('',include('index.urls')), 	# 路径匹配include，找到上一级的index目录下的urls文件
    path('',include('Douban.urls')),
]
```

现在来看include，其实就是为了加载子项目里面的urlpatterns，并做了内部处理

```python
# site-packages/django/urls/conf.py
def include(arg, namespace=None): 	# 根据上面的例子，这里的arg就是index.urls，是str类型
	if isinstance(arg, tuple):
		pass
    urlconf_module = arg
	if isinstance(urlconf_module, str):
        # import_module就是导入模块，它比import多做了些额外处理
		urlconf_module = import_module(urlconf_module) 	# 这里实际上是导入index.urls
		patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
		app_name = getattr(urlconf_module, 'app_name', app_name)
	if isinstance(patterns, (list, tuple)):
		pass
	return (urlconf_module, app_name, namespace)
```

### 3.Django源码分析之view视图的请求过程

view视图既能加载model模型中的数据，又可以通过render去渲染template模板。view视图最核心的功能就是处理用户发来的请求，并把结果返回给用户。

```python
# 找到对应的views.py

# 用户发起请求，就会产生一个request对象，它必须作为第一个参数，贯穿Django请求处理。
# manage.py里面做各种初始化加载配置文件，最后调用WSGI。WSGI接收用户请求后创建了HttpRequest对象的一个实例，即request
def myyear(request, year):
    return render(request, 'yearview.html')

def year(request, year):
    return HttpResponse(year)

# render和HttpResponse，参考path和re_path的关系，可以猜测render极有可能是HttpResponse的更高级封装。
```

HttpRequest 创建与 HttpResponse 返回是一次 HTTP 请求的标准行为。

Path 将请求传递给view视图函数，request怎么得到的？如何返回的？

HttpRequest 由 WSGI 创建，HttpResponse 由开发者创建。

View 视图抽象出的两大功能：返回一个包含被请求页面内容的 HttpResponse 对象，或者抛出一个异常，比如 Http404 。  

```python
# site-packages/django/http/request.py
class HttpRequest: 	# HttpRequest包含大量的属性和方法
    def __init__(self):
        self.GET = QueryDict(mutable=True) 	# 包含HTTP GET的所有参数
        self.POST = QueryDict(mutable=True)
        self.COOKIES = {}
        self.META = {} 	# 包含所有的HTTP头部，WSGI将http头信息（User-Agent，Cookies等）转为元信息
        self.FILES = MultiValueDict()
        ......
        
class QueryDict(MultiValueDict):
    ......
    
# 从字面意思可以看出是支持多个值的字典    
class MultiValueDict(dict):    
    ......    
    
# 以GET方式做http请求：127.0.0.1:8000/?id=1&id=2&name=wilson    
# 两个id的值想都存储下来，因此引入QueryDict，对于同一个key能存多个value。可以通过打印查看
def index(request):
	print(request.GET) 	# <QueryDict: {'id': ['1', '2'], 'name': ['wilson']}>
	return HttpResponse("Hello Django!")


# site-packages/django/utils/datastructures.py
# QueryDict 继承自 MultiValueDict，MultiValueDict 又继承自 dict
class MultiValueDict(dict):
	def __init__(self, key_to_list_mapping=()):
		super().__init__(key_to_list_mapping)
	def __repr__(self):
		return "<%s: %s>" % (self.__class__.__name__, super().__repr__())
	def __getitem__(self, key):
		......
```

### 4.Django源码分析之view视图的响应过程

```python
# 引入HttpResponse直接使用
from django.http import HttpResponse
def test1(request):
    response1 = HttpResponse() 	# 空白页面
    # HttpResponse第一个参数是返回的内容。
    # content_type="text/plain"关键字参数，把默认的内容替换掉。
    # 利用key=value，这种形式可以自定义头部信息
    response2 = HttpResponse("Any Text", content_type="text/plain") 
    return response1

# 使用HttpResponse的子类
from django.http import JsonResponse
def test2(request):    
    # JsonResponse参数是一个字典，内部使用json.dumps转为json对象
    response3 = JsonResponse({'foo':'bar'}) 	# response.content
    response3['age'] = 120 	# 当作dict使用，自定义一个头部信息
    return response3
    
# 返回错误
from django.http import HttpResponseNotFound
def test3(request):      
    response4 = HttpResponseNotFound('<h1>Page not found</h1>')
    return response4
```

#### HttpResponse子类

* HttpResponse.content：响应内容

* HttpResponse.charset：响应内容的编码

* HttpResponse.status_code：响应的状态码

* JsonResponse 是 HttpResponse 的子类，专门用来生成 JSON 编码的响应。  

### 5.Django源码分析之view视图的请求响应完整过程

![DjangoFlowchart](../../../Python训练营1期/8_1_DjangoFlowchart.png)

1. 客户端发起请求，wsgi接收该请求产生request
2. Request Middlewares（请求中间件），反爬虫，安全验证等一般放在这里
3. request到达URLConf，对路径解析
4. View Middlerwares（视图中间件），页面出错处理等
5. View视图函数
6. 使用Model里面的数据
7. 查询管理器，是Model的扩展（数据库等）
8. 上下文，view和model解耦
9. 数据需要Template渲染

a. b.c.d.返回路径，返回的Response都是由View视图生成的。

使用POST方式时，上传的数据是放在_files属性中。

中间件会做一个全局性的处理。

### 6.Django源码分析之model模型的自增主键创建

为什么自定义的模型类一定要继承models.Model？

* 不需要显示定义主键，Django会自动创建叫做id的主键；
* 自动拥有查询管理器对象 ，能使用查询管理器绑定的查询命令
* 可以使用 ORM API 对数据库、表实现 CRUD  

```python
# 作品名称和作者(主演)
class Name(models.Model):
    # id 自动创建
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    stars = models.CharField(max_length=5)
```

```python
# site-packages/django/db/models/base.py
class Model(metaclass=ModelBase): 	# metaclass：元类
	...... 
    
# site-packages/django/db/models/base.py
class ModelBase(type): 	# 元类必须继承自type
    """Metaclass for all models."""
    def __new__(cls, name, bases, attrs, **kwargs): 	# 元类一定要实现魔术方法__new__
    	super_new = super().__new__    
        ...
        return new_class 	# __new__必须返回一个类
```

### 7.Django源码分析之model模型的查询管理器

```python
def books_short(request):
	### 从 models 取数据传给 template ###
	shorts = T1.objects.all() 	# T1是模型类实例，objects是查询管理器
```

* 如何让查询管理器的名称不叫做 objects？
* 如何利用 Manager(objects) 实现对 Model 的 CRUD？
* 为什么查询管理器返回 QuerySet 对象？

```python
# site-packages/django/db/models/manager.py
class Manager(BaseManager.from_queryset(QuerySet)):
	pass
```

Manager 继承自 BaseManagerFromQuerySet 类，拥有 QuerySet 的大部分方法，get、create、filter 等方法都来自 QuerySet  

```python
# site-packages/django/db/models/manager.py
class Manager(BaseManager.from_queryset(QuerySet)):
	pass

class BaseManager:
    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
        # class_name = BaseManagerFromQuerySet
        return type(class_name, (cls,), {
        '_queryset_class': queryset_class,
        **cls._get_queryset_methods(queryset_class),
        })
    # 增加了很多方法给Manager
    @classmethod
    def _get_queryset_methods(cls, queryset_class):
```

### 8.Django源码分析之template模板的加载文件

* 模版引擎怎样通过 render() 加载 HTML 文件？目录固定为templates，放在每一个APP里面
* 模版引擎怎样对模版进行渲染？

```python
def books_short(request):
	return render(request, 'result.html', locals())

# site-packages/django/shortcuts.py
def render(request, template_name, context=None, content_type=None,status=None,using=None):
	content = loader.render_to_string(template_name, context, request,using=using)
	return HttpResponse(content, content_type, status) 	# render是HttpResponse的一个封装  
           
def render_to_string(template_name, context=None, request=None, using=None):
	if isinstance(template_name, (list, tuple)):
		template = select_template(template_name, using=using)
	else:
		template = get_template(template_name, using=using)
	return template.render(context, request)

# get_template使用了_engine_list方法获得后端模板
def _engine_list(using=None):
	# 该方法返回Template文件列表，
	# engines是一个EngineHandler类的实例
	return engines.all()           
```

### 9.Django源码分析之template模板的渲染





### 10.DjangoWeb相关功能-管理界面

管理页面的设计哲学：

* 管理后台是一项缺乏创造性和乏味的工作，Django 全自动地根据模型创建后台界面。
* 管理界面不是为了网站的访问者，而是为管理者准备的。

管理页面：127.0.0.1:8000/admin。如何创建管理页面：

1. 创建管理员账号：`$ python manage.py createsuperuser`  
2. 增加模型，比如给index增加模型：`./index/admin.py`

```python
from .models import Type, Name
# 注册模型(Type,Name)到管理页面
admin.site.register(Type)
admin.site.register(Name)
```

搭建管理页面需要注意的其他步骤：

1. settings.py中的INSTALLED_APPS有一个内置的后台管理系统`django.contrib.admin`，要使用管理系统的话，该项一定要打开，不能被注释掉
2. 新建的admin.py中，要注册的Type和Name是在models引入的，models.py中Type和Name是数据库对应的模型的类的名称
3. settings.py中的DATABASES数据库配置要正确，比如数据库是mysql，数据库名为db1

上述步骤确认完后，就可以创建管理员账号了。有些情况下，创建会失败，是因为admin的库没有同步到mysql数据库当中，需要执行`$ python manage.py migrate`

一般开发中小型项目的时候，后台的管理页面可以通过Django的admin来生成；而对于大型项目，管理页面可以像前台一样做详细的开发。

### 11.DjangoWeb相关功能-表单

表单是以POST的方式提交的。

```python
# HTML的表单格式如下，以post方式提交到result.html
<form action="result.html" method="post">
	username:<input type="text" name="username" /><br>
	password:<input type="password" name="password" /> <br>
	<input type="submit" value="登录">
</form>
```

```python
# Django使用Form对象定义表单
# form.py
from django import forms
class LoginForm(forms.Form):
	username = forms.CharField() 	# CharField标准输入框
	password = forms.CharField(widget=forms.PasswordInput, min_length=6)
```

GET方式是展示页面，POST方式是提交。某些页面既要处理GET，也要处理POST。

urlpatterns（path和view关联），view处理request，借助render将参数传递给模板里的html页面，html页面接收参数并做展示。

Django利用表单将Python中的代码转成html，这个功能和ORM很像，Model中的定义的类通过ORM转化成SQL语句。

### 12.DjangoWeb相关功能-表单CSRF防护

CSRF：跨站请求攻击

POST的时候加入csrf token，就能起到保护作用。CSRF只用作POST的请求验证

用户提交一次请求和服务端连接后，服务端的csrf token会更换，下次重新提交或被别人利用提交的话，会返回403错误。

CSRF防护是在settings.py中的MIDDDLEWARE中配置的：

django.middleware.csrf.CsrfViewMiddleware

```python
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt 	# 单独指定这个不被csrf验证。同理，@csrf_protect是单独指定被csrf验证
def result(request):
    return render(request, 'result.html')
```

特别注意的一点：除了post外，还有一种是通过Ajax提交的，这个也必须加上csrf token

### 13.DjangoWeb相关功能-用户管理认证

```python
def login2(request):
    if request.method == 'POST':
    	login_form = LoginForm(request.POST)
    	if login_form.is_valid():
    		# 读取表单的返回值
    		cd = login_form.cleaned_data
    		user = authenticate(username=cd['username'], password=cd['password'])
            # authenticate验证成功返回一个用户对象，验证失败返回None
    		if user:
    			# 登陆用户
    			login(request, user)
    			return HttpResponse('登录成功')
    		else:
    			return HttpResponse('登录失败')
```

验证的前提是已经提前注册号用户名和密码，如何注册用户？在终端下输入命令`$python manage.py shell`

```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('tom', 'tom@tom.com', 'tompwd') # objects是查询管理器
>>> user.save() 	# user是一个标准的ORM，调用save()存入数据库，具体是哪个数据库要看settings.py中DATABASE的配置，具体是哪个表要看MIDDLEWARE中验证中间件：django.contrib.auth.middleware.AuthenticationMiddleware

>>> from django.contrib.auth import authenticate
>>> user = authenticate(username='tom', password='tompwd’)
```

### 14.DjangoWeb相关功能-信号

信号：

* 发生事件，通知应用程序

* 支持若干信号发送者通知一组接收者（多个应用程序都对某一事件感兴趣时，把它们都注册到这个事件的订阅列表中。事件发生，所有的订阅者都会得到通知）

* 解耦

内建信号有哪些？https://docs.djangoproject.com/zh-hans/2.2/ref/signals/  

信号注册回调函数的方式有两种：

```python
# receiver
def my_callback1(sender, **kwargs):
    print("Request started!")
    
# 函数方式注册回调函数，使用connect
from django.core.signals import request_started 	# request_started是表示请求发起的信号
request_started.connect(my_callback1)

# 装饰器方式注册回调函数
from django.core.signals import request_finished
from django.dispatch import receiver
@receiver(request_finished)
def my_callback2(sender, **kwargs):
	print("Request finished!")
```

### 15.DjangoWeb相关功能-中间件

中间件适合在请求和返回过程当中，中间来去做拦截的事情。

Django中间件是什么？

* 全局改变输入或输出
* 轻量级的、低级的“插件”系统（插件意味着可以使用可以不适用）
* 对请求、响应处理的钩子框架  

![Django中间件](../../../Python训练营1期/8_2_Django中间件.png)

自己编写的中间件最好放在应用程序下的middleware.py文件里。然后在settings.py的MIDDLEWARE中，把自己编写的中间件添加进去，例如`index.middleware.Middle1`。Django自带的中间件顺序最好不要改动。

### 16.DjangoWeb相关功能-生产环境部署

生产环境部署 vs 开发环境部署

Django底层产生HttpRequest是通过WSGIHandler完成的，它遵循的是WSGI协议。而用户请求HTTP服务的时候，使用的是http协议。我们在终端输入`python manage.py runserver ` 启动WSGI服务器为什么能处理用户请求呢？WSGI做了一个模拟的Http，模拟的功能面对大量并发请求时会产生阻塞，导致Django效率很低。因此在正式环境下需要在Django前面放置转换器来做http到wsgi的转换，常用的转换器有：

* Apache，已经逐渐被淘汰；
* Nginx，目前Nginx+Django这样的生产环境大量在使用
* gunicorn，比Nginx效率更高，配置更简单。

安装gunicorn：`$ pip install gunicorn`

在项目目录执行：`gunicorn MyDjango.wsgi`  （MyDjango是项目名称，gunicorn会自动找依赖的包）

```python
$ gunicorn --help | more
# 几个重要的参数：
# -b ADDRESS, --bind ADDRESS 	# ADDRESS是待绑定的socket，默认是'127.0.0.1:8000'
# -w INT, --workers INT 	# 处理请求的工作进程的数量，默认是1
# --access-logfile FILE 	# 请求日志保存的位置，默认是None
# --access-logformat STRING 	# 请求日志格式
# --error-logfile FILE, --log-file FILE 	# 错误日志记录的位置
# --log-level LEVEL 		# 日志的级别[info, debug]
```

gunicorn+Django就可以作为生产环境部署了。

### 17.DjangoWeb相关功能-celery介绍

* Celery 是分布式消息队列
* 使用 Celery 实现定时任务（定时任务只是Celery功能之一）  
* 存储使用的是非关系型存储Redis（因此Celery是依赖于Redis的）

![Celery架构](../../../Python训练营1期/8_3_Celery架构.png)

#### Django和Celery结合使用

```python
# 1. Redis 安装和启动
# redis下载下来后是压缩包，首先要解压缩，然后进入文件夹，找到Makefile进行编译，然后安装 
$ make install
# 安装完后查看redis.conf配置表，里面需要注意的有：
# daemonize no 		（如果是正式环境，将其改为yes，守护进程打开）
# bind 127.0.0.1 	（如果是正式环境，将其改为0.0.0.0，任何人都可以访问）
# requirepass 123456（redis密码） 
$ redis-server /path/to/redis.conf
# 启动成功后会产生一个dump.rdb，这是redis对应的磁盘文件

# 2. 安装 Celery
$ pip install celery
$ pip install redis==2.10.6 	# 这里安装的并不是数据库，而是python版本的数据库驱动程序，python3.7不能安装redis的最新版本，最好安装2.10.6
$ pip install celery-with-redis
$ pip install django-celery   	# django可以通过admin界面去设置celery的定时任务，定时任务也可以调用django相关的功能
# 安装完后，会产生一个kombu包，里面使用async目录，因为python3.7中async是保留关键字，因此要对kombu下的async要改名，并且引用的地方也全要改名（可以改为asynchronous）
```

### 18.DjangoWeb相关功能-celery定时任务的实现

```python
# 3. 添加app
$ django-admin startproject MyDjango
$ python manager.py startapp djcron
# settings.py中添加应用
INSTALL_APPS=[
	'djcelery',
	'djcron'
]

# 4. 迁移生成表，要去创建djcelery库
$ python manage.py migrate

# 5. 配置django时区
from celery.schedules import crontab
from celery.schedules import timedelta
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://:123456@127.0.0.1:6379/' # 代理人
CELERY_IMPORTS = ('djcron.tasks') # app
CELERY_TIMEZONE = 'Asia/Shanghai' # 时区
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务调度器

# 6. 在 MyDjango 下建立 celery.py，celery初始化的设置
import os
from celery import Celery, platforms 	# __init__.py中使用绝对导入，这里的celery才能找到
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','MyDjango.settings')
app = Celery('MyDjango')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True

@app.task(bind=True) 	# 将函数封装为任务
def debug_task(self):
    print('Request:{0!r}'.format(self.request))

# 在 __init__.py 增加如下代码
# 使用绝对引入，后续使用import引入会忽略当前目录下的包
from __future__ import absolute_import 	# 这句一定要写在最上面
from .celery import app as celery_app 	# .celery表示是本地的celery文件，不是第三方的库
import pymysql
pymysql.install_as_MySQLdb()


# djcron下的tasks.py中添加两个定时任务
from MyDjango.celery import app
@app.task()
def task1():
	return 'test1'
@app.task()
def task2():
	return 'test2

# 启动 Celery
$ celery -A MyDjango beat -l info
$ celery -A MyDjango worker -l info
# 通过 admin 增加定时任务
```

### 19.Flask上下文与信号

Flask是一个微型框架，和Django走了不同的路。Flask只集成了最核心的功能：

1. WSGI协议的实现（使用了Werkzeug工具）
2. 集成了Jinja模板引擎

如果需要其他功能，只需要导入Flask相关的扩展即可。比如需要ORM，只需要导入Flask-Alchemy即可；比如想支持RestfulAPI，只需要使用Flask Rest API插件即可。

Flask和Django相同的是它们都是用MTV模式。

```python
# hello.py
from flask import Flask 	# $ pip install flask
app = Flask(__name__) 		# __name__就是当前文件名字，也是app名字
@app.route('/') 			# 通过app.route将路径和函数进行绑定
def hello_world():
	return 'Hello, World!'

$ export FLASK_APP=hello.py
$ flask run
```

Django中有request，贯穿整个请求过程，而Flask中没有request，它使用上下文。

上下文：request 上下文与 session 上下文

信号：Flask 从 0.6 开始，通过 Blinker 提供了信号支持 `pip install blinker ` 

### 20.Tornado简介与其他常见网络框架对比

Tornado既是web框架，又是底层的IO库，和Nginx、gunicorn一样，放在Django之前使用。

Tonado也可以直接去做HTTP客户端和HTTP服务端。

作为客户端，Tonado支持同步 IO 与异步 IO：

* http_client = HTTPClient()

* http_client = AsyncHTTPClient()  

```python
# sync
from tornado.httpclient import HTTPClient
def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

# async
from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future
def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future
```

利用Tonado的异步IO可以实现服务端。

```python
import tornado.ioloop
import tornado.web                              

class MainHandler(tornado.web.RequestHandler):  
    def get(self):                              
        self.write("Hello, world")
        # self.render("index.html")              

# 路由映射
application = tornado.web.Application([         
    (r"/", MainHandler),                   
])

if __name__ == "__main__":
    application.listen(8000)                    
    tornado.ioloop.IOLoop.instance().start()

# 三个底层的IO框架：
# gevent  python的并发框架，代码好维护
# twisted python的事件驱动异步框架，稳定性最好（scrapy的底层就是twisted）
# tornado 兼容性最好
```


