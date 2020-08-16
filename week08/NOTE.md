### 变量的赋值

python中一切皆对象，传递的都是对象，有的直接传递对象本身，有的传递这个对象的引用，根据传递的不同，把变量赋值做了两种划分：

* 可变数据类型（传递对象引用）：列表list，字典dict
* 不可变数据类型（传递对象本身）：整形int，浮点型float，字符串型string，元组tuple

为什么要区分可变和不可变，主要是考虑性能问题。不可变数据不管有多少个引用，都是同一块内存；缺点是改变变量值时，必须新创建对象（开辟新的内存）。可变数据，值的变化不会引起新建对象，内存地址不会变，只是内存地址里面的内容发生变化或者内存地址得到扩充。

### 容器序列的深浅拷贝

从类型的定义角度上可以把数据分为序列和非序列。

#### 序列分类

* 容器序列：list、tuple、collections.deque 等，能存放不同类型的数据；

* 扁平序列：str、bytes、bytearray、memoryview (内存视图)、array.array 等，存放的
  是相同类型的数据；

容器序列存在深拷贝、浅拷贝问题；非容器（数字、字符串、元组）类型没有拷贝问题 。 

```python
# 容器序列的拷贝问题
old_list = [ i for i in range(1, 11)]

new_list1 = old_list 	# new_list1和old_list相同
new_list2 = list(old_list) 	# 通过list类返回的new_list2是重新申请的内存，和old_list不同。new_list2 == old_list结果是True，new_list2 is old_list结果是False。

# 切片操作，也是重新申请的内存，new_list3和old_list不同
new_list3 = old_list[:]

# 嵌套对象。当给old_list增加新的元素时，new_list1和old_list一样，而new_list2，new_list3并没有增加新的元素
old_list.append([11, 12])

# 列表里面包含子列表，赋值时会产生深拷贝和浅拷贝的问题
import copy
new_list4 = copy.copy(old_list)		# 浅拷贝，只拷贝子列表的对象引用
new_list5 = copy.deepcopy(old_list) # 深拷贝，拷贝子列表的完整内容，重新申请了内存

assert new_list4 == new_list5 	# True
assert new_list4 is new_list5 	# False AssertionError

old_list[10][0] = 13 	# 将元素10（子列表）的第一个元素修改
# old_list: [1,2,3,4,5,6,7,8,9,10,[13,12]]
# new_list4: [1,2,3,4,5,6,7,8,9,10,[13,12]]
# new_list5: [1,2,3,4,5,6,7,8,9,10,[11,12]]
```

python之中，传的一切都是对象，容器传的是对象的引用。

### 字典与扩展内置数据类型

collections用来扩充python的基本类型

字典与哈希

字典中能作为key的是不可变的数据类型（int，float，string，tuple）。假设使用列表作为key，此时传给字典的只是列表的引用（只是一个地址），当列表发生变化了，字典是不知道的，所以使用可变数据类型作为key会报“unhashable type”的错误。

#### 使用collections扩展内置数据类型

collections 提供了加强版的数据类型

https://docs.python.org/zh-cn/3.6/library/collections.html

* namedtuple : 带命名的元组
* deque：双向队列
* Counter：计数器  

魔术方法实现运算符重载。

### 函数的调用

函数的专业名字叫做**可调用对象**。再次强调：函数名后不带括号，表示传递函数对象，函数名后带括号，表示函数的执行。同样的道理，对于类来说，类名后不带括号，表示类的对象，类名后带括号，表示类实例化。

```python
class Kls1(object):
    def __call__(self): 	# 实例可调用，因此可以像调用函数一样去调用示例
        return 123
    
inst1 = Kls1()
inst1() 	# 返回123，实例可调用，和函数一样
```

### 变量作用域

变量作用域也叫命名空间，命名空间就是一段有名字的内存空间，在这段空间里可以创建，修改，删除等操作。

其他高级语言对变量的使用分四个步骤：变量声明，定义类型（分配内存空间），初始化（赋值、填充内存），引用（通过对象名称调用对象内存数据）。而python不太一样，它只在模块、类、函数之中才有作用域的概念。

Python 作用域遵循 LEGB 规则（四种作用域）：

* L-Local(function)；函数内的名字空间

* E-Enclosing function locals；外部嵌套函数的名字空间（例如closure）

* G-Global(module)；函数定义所在模块（文件）的名字空间

* B-Builtin(Python)；Python 内置模块的名字空间  

LEGB主要解决变量同名不同作用域和变量顺序问题。

### 函数工具与高阶函数

#### 可变参数

```python
def func(*args, **kargs):
    print(f'args: {args}') 		# 元组形式获取其他参数
    print(f'kargs:{kargs}') 	# 字典形式获取关键字参数


func(123, 'xz', name='xvalue') 	# name是关键字参数
```

#### 偏函数

functools.partial：返回一个可调用的 partial 对象

使用方法：`partial(func, *args, **kw)`
注意：

* func 是必须参数
* 至少需要一个 args 或 kw 参数  

Django的URLconf里面，使用path将URL路径和视图去进行绑定时，就用到偏函数。

#### Lambda表达式

Lambda 只是表达式，不是所有的函数逻辑都能封装进去。Lambda 表达式后面只能有一个表达式。

实现简单函数的时候可以使用 Lambda 表达式替代；使用高阶函数的时候一般使用 Lambda 表达式 （高阶函数的参数是函数）

```python
k = lambda x   : x+1 	# 入参是x，返回值为x+1
def        k(x): return x+1

print(k(1))
```

Lambda 又称为匿名函数，像函数一样执行却没有函数名称。

#### 高阶函数

高阶：参数是函数、返回值是函数。

常见的高阶函数：map、reduce、filter、apply。apply 在 Python2.3 被移除，reduce 被放在 functools 包中，推导式和生成器表达式可以替代 map 和 filter 函数。

```python
# map
def square(x):
    return x**2

m = map(square, range(10)) 	# 第一个参数是函数（即可调用对象），将第二个参数依次传递给这个函数，map返回的是一个迭代器对象
next(m) # 依次取
list(m) # 一次性取完
[square(x) for x in range(10)] 	# 列表推导式
dir(m)

# reduce
# reduce(f, [x1, x2, x3]) = f(f(x1, x2), x3)
from functools import reduce
def add(x, y):
    return x + y

reduce(add, [1, 3, 5, 7, 9]) 	# 第一个参数是函数，将第二个参数每取一个结果和参数传递给函数
#25


# filter
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])) 	# 后面参数通过第一个参数函数进行过滤


# 偏函数
def add(x, y):
    return x + y

import functools
add_1 = functools.partial(add, 1) 	# 1作为add默认的第一个参数	
add_1(10) 	# 偏函数不能和原函数同名

import itertools
g = itertools.count()
next(g)
next(g)
auto_add_1 = functools.partial(next, g)
auto_add_1()


sorted(['bob', 'about', 'Zoo', 'Credit'])
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
```

### 闭包

#### 返回值

* 返回的关键字：return，yield
* 返回的对象：可调用对象--闭包(装饰器)  

```python
# version 1
# 函数是一个对象，所以可以作为某个函数的返回结果
def line_conf():
    def line(x):
        return 2*x+1
    return line       # return a function object 返回函数对象

my_line = line_conf()
print(my_line(5))

# version 2
# 如果line()的定义中引用了外部的变量
def line_conf():
    b = 10
    def line(x):
        return 2*x+b 	# 函数引用函数外部的变量，组成闭包
    return line       # return a function object

my_line = line_conf()
print(my_line(5))

# version 3
def line_conf():
    b = 10
    def line(x):
        '''如果line()的定义中引用了外部的变量'''
        return 2*x+b
    return line       # return a function object

b = -1
my_line = line_conf()
print(my_line(5))

# 编译后函数体保存的局部变量
print(my_line.__code__.co_varnames)
# 编译后函数体保存的自由变量
print(my_line.__code__.co_freevars)
# 自由变量真正的值
print(my_line.__closure__[0].cell_contents)

# 函数还有哪些属性
def func(): 
    pass
func_magic = dir(func)

# 常规对象有哪些属性
class ClassA():
    pass
obj = ClassA()
obj_magic = dir(obj)
# 比较函数和对象的默认属性
set(func_magic) - set(obj_magic)

# 函数名
func.__name__


# version 4
def line_conf(a, b):
    def line(x):
        return a*x + b 	# a,b,line组成闭包
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))

# version 5
# 与line绑定的是line_conf()传入的a,b
a=10
b=20
def line_conf(a, b):
    def line(x):
        return a*x + b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))
```

```python
# 内部函数对外部函数作用域里变量的引用（非全局变量）则称内部函数为闭包
# 外部函数为初次定义（定义模式），内部函数为真正的函数定义（具体模式下运行）
def counter(start=0):
   count = [start]
   def incr():
       count[0] += 1
       return count[0]
   return incr

c1 = counter(10)
print(c1()) 	# 结果：11
print(c1()) 	# 结果：12

# nonlocal访问外部函数的局部变量
# 注意start的位置，return的作用域和函数内的作用域不同
def counter2(start=0):
    def incr():
        nonlocal start
        start+=1
        return start
    return incr

c1 = counter2(5)
print(c1())
print(c1())

c2 = counter2(50)
print(c2())
print(c2())
```

### 装饰器介绍

装饰器增强而不改变原有函数。装饰器强调函数的定义态而不是运行态。

```python
# 装饰器语法糖的展开：
@decorate
def target():
	print('do something')
# 等价于：    
def target():
	print('do something')
target = decorate(target)  
```

classmethod，staticmethod，property都是装饰器。

再次强调：target 表示函数，target() 表示函数执行。

new = func 体现“一切皆对象”，函数也可以被当做对象进行赋值  。

被装饰函数三种形式：被修饰函数带参数；被修饰函数带不定长参数；被修饰函数带返回值  

```python
# PEP 318 装饰器  PEP-3129 类装饰器

# 前置问题
def func1():
    pass
a = func1 		# func1 表示函数
b = func1() 	# func1() 表示执行函数

# 装饰器, @ 语法糖
@decorate   
def func2():
    print('do sth')
# 等效于下面
def func2():
    print('do sth')
func2 = decorate(func2)

# 装饰器在模块导入的时候自动运行
# testmodule.py
def decorate(func):
    print('running in module')
    def inner():
        return func()
    return inner

@decorate
def func2():
    pass

# test.py
import testmodule
# from testmodule import func2
```

### 被装饰函数带参数和返回值的处理

使用装饰器修饰被装饰函数时，被装饰函数会被替换为装饰器的内部函数；被装饰函数如果带参数和返回值的话，装饰器的内部函数也要对参数和返回值做处理。

### Python内置装饰器

```python
# functools.wraps
# @wraps接受一个函数来进行装饰
# 并加入了复制函数名称、注释文档、参数列表等等的功能
# 在装饰器里面可以访问在装饰之前的函数的属性
# @functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
# 用于在定义包装器函数时发起调用 update_wrapper() 作为函数装饰器。 
# 它等价于 partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)。

from time import ctime,sleep
from functools import wraps
def outer_arg(bar):
    def outer(func):
        # 结构不变增加wraps
        @wraps(func) 	# inner
        def inner(*args,**kwargs):
            print("%s called at %s"%(func.__name__,ctime()))
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

@outer_arg('foo_arg')
def foo(a,b,c): 	# 不用wrap的话，foo会被替换为inner；使用wrap后，inner内部的func.__name__仍然是指foo
    """  __doc__  """
    return (a+b+c)
    
print(foo.__name__)
```

```python
# functools.lru_cache
# 《fluent python》的例子，这本书值得一读
# functools.lru_cache(maxsize=128, typed=False)有两个可选参数
# maxsize代表缓存的内存占用值，超过这个值之后，旧的结果就会被释放
# typed若为True，则会把不同的参数类型得到的结果分开保存
import functools
@functools.lru_cache() # 不使用lru_cache()的话，结果不会被缓存，执行时间会很长
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    import timeit
    print(timeit.timeit("fibonacci(6)", setup="from __main__ import fibonacci"))
```

### 对象协议与鸭子类型

Duck Typing 的概念

* 容器类型协议

  * \_\_str\_\_ 打印对象时，默认输出该方法的返回值

  * \_\_getitem\_\_、\_\_setitem\_\_、\_\_delitem\_\_ 字典索引操作

  * \_\_iter\_\_ 迭代器

  * \_\_call\_\_ 可调用对象协议，在类中实现后，实例化的对象可以像函数一样去调用 

* 比较大小的协议

  * \_\_eq\_\_

  * \_\_gt\_\_

* 描述符协议和属性交互协议

  * \_\_get\_\_

  * \_\_set\_\_

* 可哈希对象
  
* \_\_hash\_\_  
  
* 上下文管理器

  with 上下文表达式的用法，使用 \_\_enter\_\_(), \_\_exit\_\_() 实现上下文管理器  

```python
class Foo(object):
    # 用于方法返回
    def __str__(self):
        return '__str__ is called'

    # 用于字典操作
    def __getitem__(self, key):
        print(f'__getitem__ {key}') 
    
    def __setitem__(self, key, value):
        print(f'__setitem__ {key}, {value}')
    
    def __delitem__(self, key):
        print(f'__delitem__ {key}')

    # 用于迭代
    def __iter__(self):
        return iter([i for i in range(5)])


# __str__
bar = Foo()
print(bar)

# __XXitem__
bar['key1']
bar['key1']='value1'
del bar['key1']

# __iter__
for i in bar:
    print(i)
```

```python
# python输出格式的发展
firstname = 'yin'
lastname = 'wilson'
print('Hello, %s %s.' % (lastname, firstname))
print('Hello, {1} {0}.'.format(firstname, lastname))
print(f'Hello, {lastname} {firstname}.')
```

类中的魔术方法`__str__`和`__repr__`一般是相同的，不同的在于`__str__`用于字符串输出，`__repr__`用于对象传递。

```python
# typing 类型注解(type hint)，它只是类型的注解，并不是强制
# 与鸭子类型相反的是静态类型，声明变量的时候就要指定类型，如果使用其他类型对变量赋值就会报错
def func(text: str, number: int) -> str: 
    return text * number

func('a', 5)
```

### yield语句

#### 生成器

1. 在函数中使用 yield 关键字，可以实现生成器，生成器可以让函数返回可迭代对象。
2. yield 和 return 不同，return 返回后，函数状态终止，yield 保持函数的执行状态，返回后，函数回到之前保存的状态继续执行。
3. 函数被 yield 会暂停，局部变量也会被保存。
4. 迭代器终止时，会抛出 StopIteration 异常。  

```python
print([ i for i in range(0,11)]) 	# 列表推导式
# 替换为
print(( i for i in range(0,11))) 	# 列表换元组后，就变为生成器了
gennumber = ( i for i in range(0,11))
print(next(gennumber))
print(next(gennumber))
print(next(gennumber))
# print(list(gennumber)) 	# 利用list可以将生成器对象转为列表
print([i for i in gennumber ])
```

Iterables：可迭代的，包含 \_\_getitem\_\_() 或 \_\_iter\_\_() 方法的容器对象，\_\_getitem__() 底层就是通过\_\_iter\_\_() 实现的。对于可迭代的对象，可以使用for in来访问。

Iterator： 迭代器，包含 next() 和 \_\_iter\_\_() 方法，next() 底层就是通过 \_\_next\_\_() 实现的。迭代器可以通过for in访问，也可以调用next()

Generator： 生成器，包含 yield 语句的函数。

Iterables包含Iterator，Iterator又包含Generator。

```python
alist = [1,2,3,4,5]
hasattr(alist, '__iter__') 	# True
hasattr(alist, '__next__') 	# False
# hasattr用于判断对象是否有某功能，框架里面经常用到，比如先判断有没有该功能，有就直接用，没有的话通过setattr创建对应的功能再用。
# 列表可迭代，是可迭代对象，，因此可通过for in访问；但没有__next__，因此不是迭代器
for i in alist:
    print(i)
# __iter__方法是 iter() 函数所对应的魔术方法    
# __next__方法是 next() 函数所对应的魔术方法

g = (i for i in range(5)) 	# g: <generator object>
hasattr(g, '__iter__') 	# True
hasattr(g, '__next__') 	# True

g.__next__()
next(g)
for i in g:
    print(i)
# 生成器实现了完整的迭代器协议，因此即可用next，也可用for in

# 类实现完整的迭代器协议：必须要实现__iter__和__next__
class SampleIterator:
    def __iter__(self):
        return self
    
    def __next__(self):
        # not the end
        if ...:
            return ...
        # reach the end
        else:
            raise StopIteration
            
# 函数实现完整的迭代器协议：只要有yield
def SampleGenerator():
    yield ...
# 只要一个函数定义中出现了yield关键字，则此函数变为一个“生成器构造函数”，调用此构造函数即可产生一个生成器对象。

def check_iterator(obj):
    if hasattr(obj, '__iter__'):
        if hasattr(obj, '__next__'):
            print(f'{obj} is a iterator') 	# 完整迭代器协议
        else:
            print(f'{obj} is a iterable') 	# 可迭代对象
    else:
        print(f'{obj} can not iterable') 	# 不可迭代
        
def func1():
    yield range(5)
    
# 有yield的函数是迭代器，执行yield语句之后才变成生成器构造函数    
check_iterator(func1())    
```

### 迭代器使用的注意事项

```python
# itertools的三个常见无限迭代器
import itertools

count = itertoos.count() 	# 计数器
next(count)

cycle = itertoos.cycle('yes', 'no') 	# 循环遍历
next(cycle)

repeat = itertoos.repeat(10, times=2) 	# 重复
next(repeat)

# 有限迭代器
for j in itertools.chain('abc', [1,2,3]): 	# 迭代嵌套，避免用多次循环
    print(j)

# python3.3引入了 yield from，PEP-380
def chain2(*iterables):
    for i in iterables:
        yield from i	# 发现对象还能迭代，则继续迭代，替代内层循环
        
list(chain2('abc', [1,2,3]))        
```

```python
# 迭代器有效性测试
a_dict = {'a':1, 'b':2}
a_dict_iter = iter(a_dict)
next(a_dict_iter) 	# 按照key迭代
a_dict['c'] = 3
next(a_dict_iter) 	# RuntimeError: 字典进行插入操作后，字典迭代器立即失效

# 如果对列表生成迭代器，列表尾插入操作不会损坏迭代器，列表会自动变长

# 迭代器一旦耗尽，永久损坏，不可恢复
x = iter([y for y in range(5)])
for i in x:
    i
x.__next__ 	# 报StopIteration
```

### yield表达式

```python
# 通过yield返回值和传递值，yield可以暂停程序，next和send控制yield继续程序
def jumping_range(up_to):
    index = 0
    while index < up_to:
        jump = yield index
        pinrt(f'jump is {jump}')
        if jump is None:
            jump = 1
        index += jump
        print(f'index is {index}')
        
if __name__ == '__main__':
    it = jumping_range(5)
    print(next(it)) 	# 程序停在yield index处，调用next后，将index值返回，此时为0
    print(it.send(2)) 	# 将send的2赋值给jump，然后index也等于2
    print(next(it)) 	# 再次调用next相当于send(None)，jump is None成立，jump=1，index=3
    print(it.send(-1)) 	# 将send的-1赋值给jump，然后index=2
```

### 协程简介

协程经常和多线程一起出现

#### 协程和线程的区别

* 协程是异步的，线程是同步的

* 协程是非抢占式的，线程是抢占式的

* 协程是主动调度的，线程是被动调度的

* 协程可以暂停函数的执行，保留上一次调用时的状态，是增强型生成器

* 协程是用户级的任务调度，线程是内核级的任务调度

* 协程适用于 IO 密集型程序，不适用于 CPU 密集型程序的处理  

#### 异步编程

python3.5 版本引入了 await 取代 yield from 方式。

```python
import asyncio 	# 通过名字可以看出，用于异步io
async def py35_coro(): 	# 
	await stuff() 		# await必须放在函数中，此函数必须使用关键字async
```

注意： await 接收的对象必须是 awaitable 对象，awaitable 对象定义了 _\_await\_\_() 方法。

awaitable 对象有三类：

1. 协程 coroutine

2. 任务 Task

3. 未来对象 Future  

```python
import asyncio
async def main():
    print('hello')
    await asyncio.sleep(3)
    print('world')
 
# asyncio.run()运行最高层级的coroutine
asyncio.run(main())    
```

协程调用过程：调用协程时，会被注册到ioloop，返回coroutine对象；为避免大量回调，用ensure_future将coroutine对象封装为Future对象，再提交给ioloop。

官方文档 https://docs.python.org/zh-cn/3/library/asyncio-task.html

### aiohttp简介

asyncio更多偏向于底层，应用中更多使用协程完成http服务端和客户端功能：aiohttp

```python
# web server
from aiohttp import web

# views
async def index(request): 	# async表明是异步响应
    return web.Response(text='hello aiohttp') 	# 这里简单返回文字，不使用模板

# routes
def setup_routes(app):
    app.router.add_get('/', index)
    
# app
app = web.Application() 	# 实例化一个应用程序
setup_routes(app) 			# 把url和视图做绑定
web.run_app(app, host='127.0.0.1', port=8080) 	# 真正启动，事件循环和事件注册
```

```python
# web client
import aiohttp
import asyncio

url = [
    'http://httpbin.org',
    'http://httpbin.org/get',
    'http://httpbin.org/ip',
    'http://httpbin.org/headers',
]

async def crawler():
    async with aiohttp.ClientSession() as session: 	# 创建session
        futures = map(asyncio.ensure_future, map(session.get, urls))
        for task in asyncio.as_completed(futures): 	# 将future对象封装成任务
            print(await task)
            
if __name__ == '__main__':
    ioloop = asyncio.get_event_loop() 	# 获取事件循环
    ioloop.run_until_complete(asyncio.ensure_future(crawler()))
```

异步的一般流程是，有一个事件循环，在循环中注册要用的回调函数。有事件触发后，通过注册找到函数去响应。

```python
# 进程池和协程
from multiprocessing import Pool
import asyncio
import time

async def test(time):
    await asyncio.sleep(time)

async def main(num):
    start_time = time.time()
    tasks = [asyncio.create_task(test(1)) for proxy in range(num)]
    [await t for t in tasks]
    print(time.time() - start_time)
    
def run(num):
    asyncio.run(main(num))
    
if __name__ == "__main__":
    start_time = time.time()
    p = Pool() 		# 创建进程池
    for i in range(4):
        p.apply_async(run, args=(2500,)) 	# 四个进程同时运行，每个进程里面有一个协程
    p.close()
    p.join()
    print(f'total {time.time() - start_time}')
```

