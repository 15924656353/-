from selenium import webdriver  # 用于控制浏览器
from selenium.webdriver.edge.options import Options     # 用于设置微软浏览器选项
from selenium.webdriver.edge.service import Service     # 用于管理微软浏览器驱动程序
from selenium.webdriver.common.by import By     # 用于定位元素
import time
import threading

class A1:
# 定义一个函数，用于打开浏览器并返回浏览器对象
    def op(self):
        # 创建设置浏览器对象
        q1 = Options()
        # 禁用沙盒模式（增加兼容性）
        q1.add_argument('--no-sandbox')
        # 保持浏览器打开状态，默认是关闭的
        q1.add_experimental_option('detach', True)
        # 创建并启动浏览器
        driver = webdriver.Edge(service=Service(r'Selenium_i\msedgedriver.exe'), options=q1)
        driver.implicitly_wait(30) # 隐式等待，最长等待30秒
        driver.get('https://www.baidu.com/')
        return driver
    def op1(self):
        driver = self.op()
        a = driver.find_element(By.ID, 'kw')
        time.sleep(3)
        a.send_keys('python菜鸟教程')    # 输入框输入python
        time.sleep(3)
        a.clear()    # 清空输入框
        time.sleep(3)
        a.send_keys('python菜鸟教程')    # 输入框输入python
        a.click()    # 元素点击
        time.sleep(3)
threading.Thread(target=A1().op1).start()
threading.Thread(target=A1().op1).start()
threading.Thread(target=A1().op1).start()
threading.Thread(target=A1().op1).start()
# 打开指定网址
# driver.get('https://www.ihchina.cn/zhanlan')
# time.sleep(5)
# a = driver.find_element(By.ID, 'more')
# a.click()


'''a = driver.find_element(By.ID, 'kw')
time.sleep(3)
a.send_keys('python菜鸟教程')    # 输入框输入python
time.sleep(3)
a.clear()    # 清空输入框
time.sleep(3)
a.send_keys('python菜鸟教程')    # 输入框输入python
a.click()    # 元素点击
time.sleep(3)
driver.quit()'''

'''
# 浏览器查找多个元素
# document.getElementByid('kw'), 在浏览器控制台输入, 用于检查元素是否存在，有没有重复
# 定位一个元素，By的八大定位方式
a = driver.find_element(By.ID, 'kw')
# 定位多个元素,找到则返回一个列表，找不到则返回空列表
# 注意：find_elements返回的是一个列表，即使只有一个元素也会被封装成列表
a = driver.find_elements(By.ID, 'kw')
print(a)'''

'''time.sleep(3)
# driver.close()    关闭当前标签页
# 关闭浏览器
driver.quit()'''

'''
driver.maximize_window()  # 最大化浏览器窗口
driver.minimize_window()  # 最小化浏览器窗口
driver.set_window_size(800, 600)  # 设置浏览器窗口大小为800x600
driver.set_window_position(100, 100)  # 设置浏览器窗口位置为(100, 100)
'''

'''
# 浏览器截图，网页刷新
driver.refresh()  # 刷新当前页面
driver.get_screenshot_as_file('screenshot.png')  # 保存当前页面截图
'''