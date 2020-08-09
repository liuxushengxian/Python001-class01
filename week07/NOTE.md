学习笔记

### 类属性与对象属性

python当中一切皆对象。对象是一个数据以及相关行为的集合。python的类都继承自object对象。类有两大成员：属性和方法。

#### 属性

* 类属性：其字段在内存中只保存一份，属于类；直接在类下定义的字段称为静态字段，这就是类属性
* 对象属性：在每个对象都保存一份，属于对象；在实例化的方法中定义的字段，self.name=name，这就是对象属性

### 类方法描述器

方法的上面加@，称之为语法糖（相当于咖啡里面加糖，口感更好），给普通的方法加一些特殊的功能，使之更好用。

#### 三种方法

* 普通方法：至少一个self参数，表示该方法的对象（self名字可以修改，但现在是约定俗成的，不建议改）
* 类方法：至少一个cls参数，表示该方法的类（@classmethod）
* 静态方法：由类调用，无参数（@staticmethod）

三种方法在内存中都归属于类。

```python
# Foo类：
def instance_method(self):	# self会被替换为类实例化后的对象
    ...
    
@classmethod
def class_method(cls):		# cls会被替换为类
    ...
    
@staticmethod
def static_method():		# 没有参数
    ...
```

python的类有且只有一个构造函数`__new__()`，它并不能满足我们实际需要。当类需要进行一系列构造函数的时候，就可以使用类方法，它就相当于java和c++中的构造函数。

类方法用在模拟java定义多个构造函数的情况，因为python类中只有一个`__init()__`，不能按照不同的情况初始化类。

`@classmethod`使用的两大场景：

* 将其定义到父类中，子类根据自己名称的变化去使用父类的类方法；
* 当函数需要去使用类，并且返回类的时候，可以将其定义为类方法；

### 静态方法描述器

`@staticmethod`定义的静态方法，没有self和cls参数，因此它不等调用类或实例的任何属性。多数情况下，静态方法是用来做一些功能的转化。

静态方法可以由类直接调用，因为不传入self 也不传入 cls ，所以不能使用类属性和实例属性

### 描述器高级应用\_\_getattribute\_\_

类的实例的属性描述符，用于属性的赋值和读取时，做一些特殊的功能，让类的功能更高级。

#### 属性的处理

在类中，需要对实例获取属性这一行为进行操作，可以使用：`__getattribute__()`和`__getattr__()`。

相同点：都可以对实例属性进行获取拦截；

不同点：`__getattr__()`适用于未定义的属性；`__getattribute__()`对所有属性的访问都会调用该方法；

### 描述器高级应用\_\_getattr_\_

当实例的属性不在`__dict__()`之内时，才去调用`__getattr__()`，它和`__getattribute__()`有本质的区别。

需要注意的是，我们通过`__getattr__()`只是改变了它的行为，比如对不存在的属性返回OK，但是该属性还是不存在的，在`__dict__()`仍然看不到。

### 描述器原理&属性描述符

`__getattribute__()`和`__getattr__()`是上层封装的方法，它们在底层的实现是使用描述器，描述器是指实现特定协议的一组工具。

#### 属性描述符property

描述器：实现特定协议（描述符）的类。

property类需要实现`__get__,__set__,__delete__`方法。

```python
# GOD
class Human2(object):
    def __init__(self):
        self._gender = None
    # 使用@property将方法封装成属性，好处是将方法的复杂调用（考虑参数，类型等等）变为属性的简单使用
    @property 	# 这个是属性描述符，是一个类，里面实现了fget,fset,fdel等等，这三个方法的底层实现就是__get__,__set__,__delete__.
    def gender2(self):	# 使用@property将方法封装为属性后，该属性默认是只读的。要支持修改和删除还得使用别的修饰，见下。
        print(self._gender)

    # 支持修改
    @gender2.setter
    def gender2(self,value):
        self._gender = value

    # 支持删除
    @gender2.deleter
    def gender2(self):
        del self._gender


h = Human2()
h.gender = 'F'
h.gender
del h.gender
# 另一种property写法
# gender  = property(get_, set_, del_, 'other property')

# 被装饰函数建议使用相同的gender2
# 不使用setter，并不能真正意义上实现无法写入，gender被改名为 _Article__gender
```

property本质并不是函数，而是特殊类（实现了数据描述符的类）。如果一个对象同时定义了`__get__(),__set__()`，则称为数据描述符；如果仅定义了`__get__()`方法，则称为非数据描述符。

#### property优点

1. 代码更简洁，可读性、可维护性更强；
2. 更好的管理属性的访问；
3. 控制属性访问权限，提高数据安全性。

### 面向对象编程-继承

python2.2之前的类叫经典类，自定义的类和基本数据类型的类不一致；python3中的类叫新式类，所有的类都继承自object。

#### object和type的关系

* object和type都属于type类（class 'type'），type类是专门创建类的类，就好比太上皇
* type类由type元类自身创建的，object类是由元类type创建
* object的父类为空，没有继承任何类，object是所有类的基类
* type的父类为object类（class 'object'）

#### 类的继承

* 单一继承
* 多重继承：A是B的父类，B又是C的父类
* 菱形继承（钻石继承）：涉及到继承机制MRO，以及MRO的C3算法

子类的`__init__`会覆盖父类的`__init__`，子类通过`super().__init__`继承父类的属性。

```python
# 钻石继承
class Base(object):
    num_base_calls = 0
    def call_me(self):
        print("calling method on Base Class")
        self.num_base_calls += 1
        
class Left(Base):
    num_left_calls = 0
    def call_me(self):
        print("calling method on Left Class")
        self.num_left_calls += 1     
        
class Right(Base):
    num_right_calls = 0
    def call_me(self):
        print("calling method on Right Class")
        self.num_right_calls += 1   
        
class Sub(Left, Right):
    pass

a = Sub()
a.call_me()
# 此时，继承的方法按照广度优先的顺序，Left->Right->Base

print(Sub.mro()) 	# 通过mro方法可以知道继承的查找顺序
```

有向无环图DAG

### solid设计原则与设计模式&单例模式

#### SOLID设计原则（主要是SOL，前三个原则）

* 单一责任原则 The Single Responsibility Principle 类完成单一功能，否则要拆分
* 开放封闭原则 The Open Closed Principle 扩展开放，修改封闭，即尽量不修改原有的，而是在其基础上重新增加新功能。
* 里氏替换原则 The Liskov Substitution Principle 子类尽量覆盖父类的方法
* 接口分离原则 The Interface Segregation Principle   高层模块不依赖于底层模块
* 依赖倒置原则 The Dependency Inversion Principle

#### 设计模式

* 设计模式用于解决普遍性问题

* 设计模式保证结构的完整性  

#### 单例模式

1. 对象只存在一个实例

2. `__init__` 和 `__new__`（构造函数） 的区别：

   * `__new__` 是实例创建之前被调用，返回该实例对象，是静态方法

   * `__init__` 是实例对象创建完成后被调用，是实例方法

   * `__new__` 先被调用，`__init__` 后被调用

   * `__new__` 的返回值（实例）将传递给 `__init__` 方法的第一个参数，`__init__` 给这个实例设置相关参数  

### 工厂模式

#### 简单工厂模式（静态工厂模式）

根据传入的参数的不同，去创建不同的实例。它有三种角色：

* 工厂角色：判断输入参数，产生实例

* 抽象产品角色：父类，提供公共接口

* 具体产品角色：产生具体的实例

#### 类工厂模式（动态工厂模式）

```python
# 返回在函数内动态创建的类
def factory2(func):
    class klass: pass
    # setattr需要三个参数:对象、key、value
    setattr(klass, func.__name__, func) 
    # setattr(klass, func.__name__, classmethod(func)) 	# func为类的方法了
    return klass

def say_foo(self): 
    print('bar')
  
# 传入新的函数，产生一个新的类
Foo = factory2(say_foo)
foo = Foo()
foo.say_foo()    
```

类工厂模式一般变成不会用到，也就Django和Scrapy用到。

### 元类

元类是关于类的类，是类的模板。

* 元类是用来控制如何创建类的，正如类是创建对象的模板一样。

* 元类的实例为类，正如类的实例为对象

* 创建元类的两种方法

  1. class

  2. type：type（类名，父类的元组（根据继承的需要，可以为空，包含属性的字典（名字和值））  

```python
# 使用type元类创建类
def hi():
    print('Hi metaclass')

# type的三个参数:类名、父类的元组、类的成员
Foo = type('Foo',(),{'say_hi':hi}) 	# 第三个参数是字典，say_hi只是描述说明，hi才是真正的成员
foo = Foo 	# Foo是类对象，Foo()是类实例化 
foo.say_hi() 	# say_hi是函数对象，say_hi()是函数执行
```

元类type首先是一个类，所以比类工厂的方法更灵活多变，可以自由创建子类来扩展元类的能力。

```python
def pop_value(self,dict_value):
    for key in self.keys():
        if self.__getitem__(key) == dict_value:
            self.pop(key)
            break
# 元类要求，必须继承自type    
class DelValue(type):
    # 元类要求，必须实现__new__方法
    def __new__(cls,name,bases,attrs): 	# 参数是：类，名字，父类，属性。
        attrs['pop_value'] = pop_value
        return type.__new__(cls,name,bases,attrs)
 
class DelDictValue(dict,metaclass=DelValue): 	# 继承字典，同时继承一个元类DelValue
    # python2的用法，在python3不支持
    # __metaclass__ = DelValue
    pass

d = DelDictValue()
d['a']='A'
d['b']='B'
d['c']='C'
d.pop_value('C') 	# 通过value来移除对应key-value
for k,v in d.items():
    print(k,v)
```

### mixin模式

#### 抽象基类

抽象基类（abstract base class，ABC）用来确保派生类实现了基类中的特定方法。

使用抽象基类的好处：

* 避免继承错误，使类层次易于理解和维护。

* 无法实例化基类。

* 如果忘记在其中一个子类中实现接口方法，要尽早报错。

```python
from abc import ABC
class MyABC(ABC):
	pass
MyABC.register(tuple)
assert issubclass(tuple, MyABC)
assert isinstance((), MyABC) 
```

```python
from abc import ABCMeta, abstractmethod
class Base(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass
    @abstractmethod
    def bar(self):
        pass

class Concrete(Base): 
    def foo(self):
        pass
# Concrete没有实现bar方法，因此下面会报错
c = Concrete() # TypeError
```

#### Mixin模式

在程序运行过程中，重定义类的继承，即动态继承。好处：

* 可以在不修改任何源代码的情况下，对已有类进行扩展；
* 进行组件的划分  

```python
def mixin(Klass, MixinKlass):
    # 将Mixinklass作为Klass的父类，动态改变Klass的继承关系
    Klass.__bases__ = (MixinKlass,) + Klass.__bases__

class Fclass(object):
    def text(self):
        print('in FatherClass')

class S1class(Fclass):
    pass

class MixinClass(object):
    def text(self):
        # return super().text()
        print('in MixinClass')

class S2class(S1class, MixinClass):
    pass

print(f' test1 : S1class MRO : {S1class.mro()}')
s1 = S1class()
s1.text()

mixin(S1class, MixinClass)
print(f' test2 : S1class MRO : {S1class.mro()}')
s1 = S1class()
s1.text()

print(f' test3 : S2class MRO : {S2class.mro()}')
s2 = S2class()
s2.text()

```

