# -*- coding: utf-8 -*-
# @Project : PyCharm
# @Time    : 2019/3/15 17:00
# @Author  : tangzhou
# @File    : thread_test.py
# @Software: PyCharm Community Edition
# @Contact : 505200187@qq.com
# @desc    :
import threading
import time
import os
import asyncio
def booth(tid):
    global i
    global lock
    while True:
        lock.acquire()
        if i!=0:
            i=i-1
            print("窗口:",tid,",剩余票数:",i)
            time.sleep(1)
        else:
            print("Thread_id",tid,"No more tickets")
            os._exit(0)
        lock.release()
        time.sleep(1)

i = 100
lock=threading.Lock()
def a():
    print("1111")
a()
#---------------------------------------------------------------------------------------
# 多线程调用协程，可以使用new_event_loop，set_event_loop。不能用new
#--------------------------------------------------------------------------------------
async def bbb():
    await ccc()
    print('bbbb')
async def ccc():
    print('cccc')
    await asyncio.sleep(1)

def aaa(a):
    # 线程中必须用new不能get
    loop = asyncio.new_event_loop()
    # asyncio.get_event_loop()
    res = loop.run_until_complete(bbb())
    loop.close()
th=[]
for k in range(3):

    new_thread = threading.Thread(target=aaa,args=(1,))
    th.append(new_thread)
    new_thread.start()
print('111')
for i in th:
    i.join(10)
print('2222')
#---------------------------------------------------------------------------------------
# 启动上述代码之后，当前线程不会被block，
# 新线程中会按照顺序执行call_soon_threadsafe方法注册的more_work方法，
# 后者因为time.sleep操作是同步阻塞的，因此运行完毕more_work需要大致6 + 3
# **这是调用一个简单的方式就是使用多线程。当前线程创建一个事件循环，**
# **然后在新建一个线程，在新线程中启动事件循环。当前线程不会被block。**
#--------------------------------------------------------------------------------------
# import asyncio
# from threading import Thread
# import time
#
# now = lambda :time.time()
#
# def start_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()
#
# def more_work(x):
#     print('More work {}'.format(x))
#     time.sleep(x)
#     print('Finished more work {}'.format(x))
#
# start = now()
# new_loop = asyncio.new_event_loop()
# t = Thread(target=start_loop, args=(new_loop,))
# t.start()
# print('TIME: {}'.format(time.time() - start))
#
# new_loop.call_soon_threadsafe(more_work, 6)
# new_loop.call_soon_threadsafe(more_work, 3)
# print('TIME: {}'.format(time.time() - start))

#---------------------------------------------------------------------------------------
# 主线程中创建一个new_loop，然后在另外的子线程中开启一个无限事件循环。
#  主线程通过run_coroutine_threadsafe新注册协程对象。这样就能在子线程中进行事件循环的并发操作，
# 同时主线程又不会被block。一共执行的时间大概在6s左右。
# **这是调用一个简单的方式就是使用多线程。当前线程创建一个事件循环，**
# **然后在新建一个线程，在新线程中启动事件循环。当前线程不会被block。**
#--------------------------------------------------------------------------------------
import asyncio
import time
from threading import Thread

now = lambda :time.time()


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def do_some_work(x):
    print('Waiting {}'.format(x))
    await asyncio.sleep(x)
    print('Done after {}s'.format(x))

def more_work(x):
    print('More work {}'.format(x))
    time.sleep(x)
    print('Finished more work {}'.format(x))

start = now()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()
print('TIME: {}'.format(time.time() - start))

asyncio.run_coroutine_threadsafe(do_some_work(6), new_loop)
asyncio.run_coroutine_threadsafe(do_some_work(4), new_loop)
# asyncio.get_event_loop()


# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time

driver = webdriver.Chrome()
driver.get("https://www.baidu.com/")
driver.implicitly_wait(20)

mouse = driver.find_element_by_link_text("设置")
ActionChains(driver).move_to_element(mouse).perform()
driver.find_element_by_link_text("搜索设置").click()
time.sleep(2)
# 实例化select
s = Select(driver.find_element_by_id("nr"))
# 定位选项
s.select_by_value("20")  # 选择value="20"的项：通过value属性
time.sleep(2)  # 为了明显的看出变化
s.select_by_index(0)  # 选择第一项选项：通过选项的顺序选择，第一个为 0
time.sleep(2)  # 为了明显的看出变化
s.select_by_visible_text("每页显示50条")  # 选择text="每页显示50条"的值，即在下拉时我们可以看到的文本

