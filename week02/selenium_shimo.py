# -*- coding:utf8 -*-

import time
import pyautogui
from selenium import webdriver

usr = pyautogui.prompt(text='输入注册手机号或邮箱', title='登录')
pwd = pyautogui.password(text='输入密码', title='登录', mask='*')

browser = webdriver.Chrome()
browser.get('https://shimo.im/login?from=home')
time.sleep(1)

browser.find_element_by_xpath('//div[@class="main"]/div[2]/div/div/div/div[1]/div/input').send_keys(usr)
browser.find_element_by_xpath('//div[@class="main"]/div[2]/div/div/div/div[2]/div/input').send_keys(pwd)
time.sleep(1)
browser.find_element_by_xpath('//div[@class="main"]/div[2]/div/div/div/button').click()
time.sleep(10)
browser.close()