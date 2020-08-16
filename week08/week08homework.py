# homework1
# 区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：
# list      容器序列，可变序列
# tuple     容器序列，不可变序列
# str       扁平序列，不可变序列
# dict      容器序列，可变序列
# collections.deque     容器序列，可变序列



# homework2
# 自定义一个 python 函数，实现 map() 函数的功能。
def my_map(func, zone): 
    for i in zone:
        yield func(i)



# homework3
# 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
import time
import random
def timer(func):
    def time_stat(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        print(time.time() - start)
        return ret
    return time_stat

@timer
def test_func(*args, **kwargs):
    time.sleep(random.randint(1,4))    



if __name__ == "__main__":
    m = my_map(lambda r: r ** 2, (1, 2, 3))
    print(list(m))
    test_func(10)
    test_func('abc', 123)
