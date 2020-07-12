# 学习笔记

### 一、Scrapy并发参数优化

#### settings.py 参数调优

```python
# 最大并发连接数（默认16），取值要考虑到发起端机器性能和服务器承受能力
CONCURRENT_REQUESTS = 32

# 每一批次下载的延时，防止爬取过快
DOWNLOAD_DELAY = 3

# 针对域名和IP的最大并发连接数
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16
```

#### 基于Twisted的异步IO框架

Twisted是异步编程模型，任务之间互相独立，用于大量I/O密集操作。

Twisted内部是一个Reactor Loop，如果请求有结果返回，通过callback来处理结果。

### 二、多进程：进程的创建

多进程、多线程、协程的目的就是为了尽可能多处理任务。

进程A创建了进程B，A和B为父子关系。

```python
# 产生新的进程的两种方式
os.fork()	# 只能支持Linux和Mac（因为os模块跟操作系统重度关联）
multiprocessing.Process()
```

```python
# multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})
# 参数说明：
# - group：进程分组，实际上很少使用
# - target：表示调用对象，即创建的进程所要执行的函数。注意这里要的是对象，传递函数名即可，后面不能跟()
# - name：别名，相当于给这个进程取一个名字
# - args：表示调用对象的参数元组，比如target是函数f，他有两个参数m，n，那么args就传入(m, n)即可
# - kwargs：表示调用对象的字典

from multiprocessing import Process

def f(name):
    print(f'hello {name}')

if __name__ == '__main__':
    p = Process(target=f, args=('john',))
    p.start()	# 子进程执行
    p.join()	# 将子进程合并到主进程，即等待子进程结束后，父进程再结束
# join也可以带timeout参数：join([timeout])
# 如果可选参数 timeout 是 None （默认值），则该方法将阻塞，直到调用 join() 方法的进程终止。
# 如果 timeout 是一个正数，它最多会阻塞 timeout 秒。
# 请注意，如果进程终止或方法超时，则该方法返回 None 。
# 检查进程的 exitcode 以确定它是否终止。
# 一个进程可以合并多次。
# 进程无法合并自身，因为这会导致死锁。
# 尝试在启动进程之前合并进程是错误的，即p.join()在p.start()之前
```

### 三、多进程调试技巧

window下vscode，Ctrl + / 可以快速注释掉某一行或多行。

利用print打印和注释来进行调试。

更高级的调试要利用内置函数：

```python
def debug_info(title):
    print(title)
    print(__name__) 		# 模块名称
    print(os.getppid()) 	# 父进程id
    print(os.getpid())		# 当前进程id

def f(name):
    debug_info('function f')

if __name__ == '__main__':
    debug_info('main')
    p = Process(target=f, args=('bob',))		# 使用函数来创建子进程
    p.start
    
	for p in multiprocessing.active_children():		# 当前活动的子进程
    	print(f'子进程名称：{p.name}' id：{str(p.pid)})
    
    print(f'CPU核的数目：{str(multiprocessing.cpu.count())}')
    # 一般多进程的数量 = cpu核的数目
    
    p.join()    
```

也可以通过继承类的方式创建进程

```python
from multiprocessing import Process

class NewProcess(Process): 	# 继承Process类创建一个新类
    def __init__(self,num):
        self.num = num
        super().__init__()

    def run(self):  # 重写Process类中的run方法.
        while True:
            print(f'我是进程 {self.num} , 我的pid是: {os.getpid()}')
            time.sleep(1)

for i in range(2):
    p = NewProcess(i)
    p.start()
# 当不给Process指定target时，会默认调用Process类里的run()方法。
# 这和指定target效果是一样的，只是将函数封装进类之后便于理解和调用。
```

### 四、多进程通信：队列

全局变量在多个进程中不能共享，在子进程中修改全局变量对父进程中的全局变量没有影响。因为父进程在创建子进程时对全局变量做了一个备份，此后父进程的全局变量和子进程的全局变量是完全独立的。各个进程的堆栈是相互独立的，因此我们不能通过变量在进程间通向数据。

进程间的共享方式包括：队列、管道、共享内存。

多个进程对共享资源的访问要用加锁机制。

队列是最常用的进程间通信方式，队列是线程和进程安全的。

```python
from multiprocessing import Process, Queue
# multiprocessing中的Queue类是一个近似queue.Queue（多线程）的克隆
# 现在有两个进程，一个进程负责写(write)，一个进程负责读(read)
# write()将写完的数据交给队列，再由队列交给read()
def f(q):
    q.put([42, None, 'hello'])	# 写入一个列表

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # 打印结果为"[42, None, 'hello']"
    p.join()
```

初始化队列时，有个参数叫maxsize（默认为0，表示不限制大小，受内存限制）。实际工作中，要指定队列的最大值。put和get有两个很重要的参数：blocked，timeout。

* 对于get：
  * blocked = True，get允许被阻塞，如果队列空，等待timeout，如果队列还是空，抛出Queue.empty异常
  * blocked = False，如果队列不为空（get可以操作）；如果队列为空，立即返回Queue.empty异常

* 对于put：
  * blocked = True，put允许被阻塞，如果队列满，等待timeout，如果队列还是满，抛出Queue.full异常
  * blocked = False, 如果队列不满（put可以操作）；如果队列满，直接返回Queue.full异常

### 五、多进程通信：管道和共享内存

#### 管道

队列的底层就是管道（Pipe）。

Pipe() 函数返回两个连接对象，它们由管道连接，默认情况下是双工（双向）。每个连接对象都有send()和recv()方法。

注意：如果两个进程（或线程）同时尝试读取或写入管道的同一 端，则管道中的数据可能会损坏。当然，同时使用管道的不同端的进程不存在损坏的风险。

实际工作中经常会遇到多个进程写入，多个进程读取的情况，此时管道的缺陷无法适应，因此实际中很少用管道，还是用队列。

```python
from multiprocessing import Process, Pipe
def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
```

#### 共享内存

多个进程共享一块内存。

共享内存 shared memory 可以使用 Value 或 Array 将数据存储在共享内存映射中。这里的Array和numpy中的不同，它只能是一维的，不能是多维的。Array和Value使用时需要定义数据形式，否则会报错。

```python
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in a:
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)			# 'd' 表示双精度浮点数
    arr = Array('i', range(10))		# 'i' 表示有符号整数
	# 'd' 和 'i' 参数是 array 模块使用的类型的 typecode
    # 共享对象 num 和 arr 是进程和线程安全的
    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
```

### 六、多进程：锁

进程安全和线程安全指的就是访问共享资源时没有发生混乱，符合我们预期。

多进程的运行是由操作系统调度的，人为不能干预。

```python
import multiprocessing as mp
import time

# 在job()中设置进程锁的使用，保证运行时一个进程的对锁内内容的独占
def job(v, num, l):
    l.acquire() # 锁住
    for _ in range(5):		# '_'表示只是想循环指定次数，对容器内取出的对象不关心
        time.sleep(0.1) 
        v.value += num 		# 获取共享内存
        print(v.value, end="|")
    l.release() # 释放

def multicore():
    l = mp.Lock() 			# 定义一个进程锁
    v = mp.Value('i', 0) 	# 定义共享内存
    # 进程锁的信息传入各个进程中
    p1 = mp.Process(target=job, args=(v,1,l)) 
    p2 = mp.Process(target=job, args=(v,3,l)) 
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    multicore()

# 运行一下，让我们看看是否还会出现抢占资源的情况
# 显然，进程锁保证了进程p1的完整运行，然后才进行了进程p2的运行

# 在某些特定的场景下要共享string类型，方式如下：
from ctypes import c_char_p
str_val = mp.Value(c_char_p, b"Hello World")
```

### 七、多进程：进程池

```python
# Pool 类表示一个工作进程池，如果要启动大量的子进程，可以用进程池的方式批量创建子进程
from multiprocessing.pool import Pool
from time import sleep, time
import random
import os

def run(name):
    print("%s子进程开始，进程ID：%d" % (name, os.getpid()))
    start = time()
    sleep(random.choice([1, 2, 3, 4]))
    end = time()
    print("%s子进程结束，进程ID：%d。耗时0.2%f" % (name, os.getpid(), end-start))

if __name__ == "__main__":
    print("父进程开始")
    # 创建多个进程，4表示可以同时执行的进程数量。默认大小是CPU的核心数
    p = Pool(4) 
    for i in range(10):
        # 创建进程，放入进程池统一管理
        p.apply_async(run, args=(i,))	# apply_async表示异步方式，apply为同步方式
    # 如果用进程池，在调用join()之前必须要先close()，而且close()之后不能再继续往进程池添加新的进程
    # 如果join()之前没有close()或者terminate()，会造成死锁
    p.close()
    # 进程池对象调用join，会等待进程池中所有的子进程结束后再去结束父进程
    p.join()
    print("父进程结束。")
    # terminate()：一旦运行到此步，不管任务是否完成，立即终止。
    p.terminate()
```

下面对进程池做进一步扩展，超时怎么处理，如何获取子进程的结果

```python
from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:         # 进程池包含4个进程
        result = pool.apply_async(f, (10,)) # 执行一个子进程
        print(result.get(timeout=1))        # 显示执行结果

        result = pool.apply_async(time.sleep, (10,))
        print(result.get(timeout=1))        # raises multiprocessing.TimeoutError
```

单进程并发：Map（映射）

```python
from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:         # 进程池包含4个进程

        print(pool.map(f, range(10)))       # 输出 "[0, 1, 4,..., 81]"
                    
        it = pool.imap(f, range(10))        # map输出列表，imap输出迭代器
        print(it)               
        print(next(it))                     #  "0"
        print(next(it))                     #  "1"
        print(it.next(timeout=1))           #  "4" 
```

### 八、多线程：创建线程

和其他语言不一样，Python中的多线程是有瓶颈和限制的，所以Python中经常是多进程和多线程混合使用，另外Python还有协程。

进程是一个比较重的概念，多进程会带来很重的资源开销；多线程是运行在一个进程里的，多线程之间同步数据就比多进程方便很多，因为内存是共用的。

阻塞和非阻塞是发起方的概念，发起方建立进程或线程后，是一直等还是可以去干别的事。

同步和异步是接收方的概念，接收方马上响应还是过段时间响应（收到消息或事件后）。

同步阻塞、同步非阻塞、异步阻塞、异步非阻塞是描述两端的行为。

Python的多线程只能在一个CPU或者一个物理核心上去运行，多进程可以运行在多个CPU上。

多进程和多线程都是由操作系统来控制的，引入协程，可以由用户来对进程切换进行把控。

多线程是并发模式，只有一个CPU资源；多进程是并行模式，每个进程有独立的cpu资源。

多线程的创建要使用threading模块：

* 使用函数创建多线程（面向过程）：`threading.Thread(target=run, args=("thread 1",))`
* 使用类创建多线程模型（面向对象）：`class MyThread(threading.Thread)`

```python
import threading

# 这个函数名可随便定义
def run(n):
    print("current task：", n)

if __name__ == "__main__":
    t1 = threading.Thread(target=run, args=("thread 1",))
    t2 = threading.Thread(target=run, args=("thread 2",))
    t1.start()
    t2.start()

# 调用方
# 阻塞  得到调用结果之前，线程会被挂起
# 非阻塞 不能立即得到结果，不会阻塞线程

# 被调用方 
# 同步 得到结果之前，调用不会返回
# 异步 请求发出后，调用立即返回，没有返回结果，通过回调函数得到实际结果

# 线程内置方法
t1.getName()	# 获取线程名字
t1.is_alive()	# 线程是否存活
```

### 九、多线程：线程锁

* 普通锁：Lock（不可嵌套），RLock（可嵌套）
* 高级锁：信号量，事件，条件锁

```python
import threading
import time

num = 0

# Lock普通锁不可嵌套，RLock普通锁可嵌套
mutex = threading.Lock()
mutex2 = threading.RLock()

class MyThread(threading.Thread):
    def run(self):
        global num
        time.sleep(1)

        if mutex.acquire(1): 	# 加锁 
            num = num + 1
            print(f'{self.name} : num value is {num}')
        mutex.release() 		# 解锁

class MyThread2(threading.Thread):
    def run(self):
        if mutex2.acquire(1):
            print("thread " + self.name + " get mutex")
            time.sleep(1)
            mutex2.acquire()
            mutex2.release()
        mutex2.release()

if __name__ == '__main__':
    for i in range(5):
        t = MyThread()
        t.start()
        

# 条件锁：该机制会使线程等待，只有满足某条件时，才释放n个线程
c = threading.Condition()
conn.acquire()
conn.wait_for(condition)  # 这个方法接受一个函数的返回值
conn.release()

# 信号量：内部实现一个计数器，占用信号量的线程数超过指定值时阻塞
semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行
semaphore.acquire()
semaphore.release()

# 事件： 定义一个flag，set设置flag为True ，clear设置flag为False
event = threading.Event()
event.clear()
event.set()
e.wait() 	# 检测当前event是什么状态，如果是False则阻塞，如果是True则继续往下执行。默认是False。

# 定时器： 指定n秒后执行
from threading import Timer
def hello():
    print("hello, world")
t = Timer(1, hello)  # 表示1秒后执行hello函数
t.start()
```

### 十、多线程：队列

Python内置的库queue：

* Queue：普通队列
* PriorityQueue：优先级队列，每个元素都是元组，`q.put((1,"work"))`，数字越小优先级越高，同优先级先进先出
* LifoQueue：后进先出队列，类似栈
* deque：双向队列，两端都可以读写，既有队列的功能，也有栈的功能

```python
import queue
q = queue.Queue(5)
q.put(111)        # 存队列
q.put(222)
 
print(q.get())    # 取队列
print(q.get())
q.task_done()     # 每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，
                  # 以提示q.join()是否停止阻塞，让线程继续执行或者退出
print(q.qsize())  # 队列中元素的个数， 队列的大小
print(q.empty())  # 队列是否为空
print(q.full())   # 队列是否满了

# 利用锁和队列实现“生产者-消费者”模型
import queue
import threading
import random
import time

writelock = threading.Lock()

class Producer(threading.Thread):
    def __init__(self, q, con, name):
        super(Producer, self).__init__()
        self.q = q
        self.name = name
        self.con =con
        print(f'Producer {self.name} Started')
    
    def run(self):
        while 1:
            global writelock
            self.con.acquire()  # 获得锁对象

            if self.q.full():   # 队列满
                with writelock:
                    print('Queue is full , producer wait')
                self.con.wait()  # 等待资源
            
            else:
                value = random.randint(0,10)
                with writelock:
                    print(f'{self.name} put value {self.name} {str(value)} in queue')
                self.q.put( (f'{self.name} : {str(value)}') ) # 放入队列
                self.con.notify()   # 通知消费者
                time.sleep(1)
        self.con.release()

class Consumer(threading.Thread):
    def __init__(self, q, con, name):
        super(Consumer, self).__init__()
        self.q = q
        self.name = name
        self.con =con
        print(f'Consumer {self.name} Started')

    def run(self):
        while 1:
            global writelock
            self.con.acquire()
            if self.q.empty():   # 队列空
                with writelock:
                    print('Queue is empty , consumer wait')
                self.con.wait()  # 等待资源
            else:
                value = self.q.get()
                with writelock:
                    print(f'{self.name} get value {value} from queue')              
                self.con.notify()   # 通知生产者
                time.sleep(1)
        self.con.release()

if __name__ == '__main__':
    q = queue.Queue(10)
    con = threading.Condition()   # 条件变量锁

    p1 = Producer(q, con, 'P1')
    p1.start()
    p2 = Producer(q, con, 'P2')
    p2.start()
    c1 = Consumer(q, con, 'C1')
    c1.start()
```

### 十一、多线程：线程池

一般的线程池：`from multiprocessing.dummy import Pool as ThreadPool`

并行任务的高级封装（Python3.2以后支持）：`from concurrent.futures import ThreadPoolExecutor`

```python
# Python3.2 中引入了 concurrent.futures 库，利用这个库可以非常方便的使用多线程、多进程
from concurrent.futures import ThreadPoolExecutor
import time

def func(args):
    print(f'call func {args}')
    
if __name__ == "__main__":
    seed = ['a', 'b', 'c', 'd']

    with ThreadPoolExecutor(3) as executor:
        executor.submit(func, seed) 	# submit会将seed原样传给函数对象func，seed是列表，传进去的还是列表
    
    time.sleep(1)

    with ThreadPoolExecutor(3) as executor2:
        executor2.map(func, seed)		# map会做一个映射，将seed列表拆开，分四次传递给func
    
    time.sleep(1)

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(pow, 2, 3)	# submit可以直接传参，不用封装为元组
        print(future.result())
```

### 十二、多线程：GIL锁与多线程性能瓶颈

Python中的多线程受GIL限制，同一时间只有一个线程在运行，所以说它是伪多线程。

GIL全局解释锁（Global Interpreter Lock）：

* 每个进程只有一个GIL锁
* 拿到GIL锁的线程可以使用CPU
* CPython解释器不是真正意义的多线程，属于伪并发

和单进程相比，多线程对于CPU密集型几乎是一样的；对于I/O密集型应用（爬虫，读写磁盘，网络通信），多线程是有优势的。