## week2学习笔记

#### 异常处理机制的原理

* 异常也是一个类
* 异常捕获过程：
  1. 异常类把错误消息打包到一个对象
  2. 然后该对象会自动查找调用栈
  3. 直到运行系统找到明确声明如何处理这些类异常的位置

* 所有异常继承自BaseException
* Traceback显示了出错的位置，显示的顺序和异常信息对象传播的方向是相反的。异常信息在Traceback信息的最后一行，有不同的类型
* 捕获异常使用try...except语法，try...except支持多重异常处理

* 常见的异常类型有：

  1. LookupError下的IndexError和KeyError

  2. IOError

  3. NameError

  4. TypeError

  5. AttributeError

  6. ZeroDivisionError

#### 使用PyMySQL进行数据库操作

一般流程：创建connection->获取cursor->CRUD（增删改查）->关闭cursor->关闭connection

#### 反爬虫

浏览器基本行为

1. 带http头信息：如User-Agent、Referer等
2. 带cookies（包含加密的用户名、密码验证信息）

User-Agent是浏览器信息，使用fake-useragent库。

Referer包含当前页面是从哪个页面跳转过来的，防止跨站。

cookies是有有效期的。一般来说大部分的网站可以直接复制cookies到代码中直接使用。

POST方式模拟用户登录，刚好和Scrapy的start_urls第一次发起请求能适配上，得到cookies。

#### 中间件和代理IP

Downloader Middlewares，从引擎到下载器经过多个下载中间件（优先级从小到大），从下载器返回也经过这些中间件（优先级从大到小）。

同一个IP并发爬虫可能导致IP被封，可以通过下载中间件修改为代理IP。

`scrapy crawl xxx --nolog` 执行后不打印log。

增加代理IP的步骤：

1. 设置代理IP，`export http_proxy='http://52.179.231.206:80'` （linux和mac）
2. settings.py中 增加 scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware
3. 通过 Request.meta['proxy'] 读取 http_proxy环境变量加载代理

settings.py中DOWNLOADER_MIDDLEWARES打开，各个功能后面的数字就是优先级，数字越小优先级越高。优先级也可以设置为None，表明不使用。

如果不想使用Scrapy自带的中间件，也可以在middlewares.py中自己实现中间件，建议不要直接在middlewares.py中修改中间件类，而是继承中间件类，然后自行修改。

##### 下载中间件

如何编写一个下载中间件？一般需要重写下面四个方法：

`process_request(request,spider)`Request对象经过下载中间件时会被调用，优先级高的先调用

`process_response(request,response,spider)`Response对象经过下载中间件时会被调用，优先级高的后调用

`process_exception(request,exception,spider)`当process_request和process_response抛出异常时会被调用

`from_crawler(cls,crawler)`使用crawler来创建中间件对象，并（必须）返回一个中间件对象

##### 具体实现

在settings.py中增加代理IP，同时将系统自带的代理中间件屏蔽（优先级设为None），使用自定义的随机HTTP代理IP中间件RandomHttpProxyMiddleware，优先级400，比默认的543高.

自定义中间件RandomHttpProxyMiddleware的实现在middlewares.py中，在该文件中，系统自带的有两个，一个是爬虫中间件，一个是下载中间件，我们不用，折叠起来。RandomHttpProxyMiddleware继承HttpProxyMiddleware类，重写`__init__,from_crawler,_set_proxy`