
from bs4 import BeautifulSoup
import pymysql
import re
import requests
import time
import threading
from selenium import webdriver  # 用于控制浏览器
from selenium.webdriver.edge.options import Options     # 用于设置微软浏览器选项
from selenium.webdriver.edge.service import Service     # 用于管理微软浏览器驱动程序
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By     # 用于定位元素
from selenium.common.exceptions import TimeoutException  # 导入超时异常类
from myspider.myspider.spiders.spider import SpiderSpider  # 导入自定义的爬虫类
from scrapy.crawler import CrawlerProcess  # 导入爬虫进程类
from queue import Queue 

class info:  
    def op(self, web_url):  
        # 创建设置浏览器对象  
        q1 = Options()  
        # 禁用沙盒模式（增加兼容性）  
        q1.add_argument('--no-sandbox')  
        # 保持浏览器打开状态，默认是关闭的  
        q1.add_experimental_option('detach', True)  
        # 创建并启动浏览器  
        driver = webdriver.Edge(service=Service(r'Selenium_i\msedgedriver.exe'), options=q1)  
        driver.implicitly_wait(30) # 隐式等待，最长等待30秒 
        driver.set_page_load_timeout(30)  # 设置页面加载超时时间为30秒 
        try:
            driver.get(web_url)  # 不需要headers，Selenium会自动处理
        except TimeoutException:
            print(f"页面加载超时: {web_url}")
            driver.quit()
            return None
        driver.minimize_window()  # 最小化浏览器窗口
        time.sleep(5)
        return driver 

    # 获取视频页面的URL列表  
    def page_url(self, page_num, return_list, web_url):  
        driver = self.op(web_url)  
        urls = []  # 创建一个空列表以存储所有的url  
        # 显式等待  使用 WebDriverWait 替代隐式等待，确保在操作元素之前它们是可见和可点击的。具体在获取输入框和按钮的部分添加了显式等待  
        wait = WebDriverWait(driver, 10)   
        for i in range(page_num, page_num + 6):  
            # 显式等待输入框可见  
            a = wait.until(EC.visibility_of_element_located((By.ID, 'page_num')))
            time.sleep(1)  
            a.clear()  # 清空输入框
            time.sleep(1)
            a = wait.until(EC.visibility_of_element_located((By.ID, 'page_num')))  # 重新定位
            time.sleep(1)
            a.send_keys(str(i))  # 输入页码  
            time.sleep(1)  # 可选的短暂延迟  
            
            # 显式等待按钮可点击  
            c = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="page-btn"]')))  
            c.click()  # 元素点击  
            time.sleep(3)  # 等待页面加载完  

            html = driver.page_source  # 获取网页源代码  
            soup = BeautifulSoup(html, "html.parser")  
            paginator = soup.find_all("tr")  # 找到包含视频信息的div元素  
            
            if paginator:  # 如果找到了tr元素  
                for row in paginator:  # 将内层循环变量改为 row  
                    url = re.findall('href="(.*?)"', str(row))  # 找到每个tr中的url  
                    if url:  # 检查url是否找到   
                        urls.extend(url)  # 添加找到的所有url  
            time.sleep(10)  # 控制请求频率，等待3秒  
        driver.quit()  # 关闭浏览器  
        return_list.append(urls)  # 将当前线程的结果添加到共享列表中   
 
    # 调用scrapy爬虫并将结果放入队列
    def run_spider(self, urls, info_all):
        process = CrawlerProcess()
        full_urls = ['https://www.ihchina.cn' + url for url in urls]   # 构造完整的URL列表
        process.crawl(SpiderSpider, urls=full_urls, info_all=info_all)
        print("开始爬取...")
        process.start()

    # 主函数，用于启动多线程并收集结果  
    def main(self):  
        web_url = 'https://www.ihchina.cn/project.html'  
        threads = []  
        results = []  # 用于存储所有线程的返回结果  
        info_all = []       # 用于接收每个页面的信息，存储到数据库时使用  
        data_queue = Queue()  # 创建一个用于存储爬虫数据的队列
        
        # 创建并启动线程  
        for num in range(230, 236, 6):   
            thread = threading.Thread(target=self.page_url, args=(num, results, web_url))  
            threads.append(thread)  
            thread.start()  
            time.sleep(2)  # 控制请求频率，等待2秒再启动下一个线程  
        
        # 等待所有线程完成  
        for thread in threads:  
            thread.join()  

        # 调用run_spider函数，运行scrapy爬取静态网页
        if results:
            urls = [*results[0],*results[1],*results[2],*results[3],*results[4]]
            self.run_spider(urls, data_queue)
    
        # 从数据队列收集结果  
        while not data_queue.empty():  
            info_all.append(data_queue.get()) 
                 
        print(len(results))   # 打印所有收有收集到的项目条数信息
        print(len(results[0]))  # 打印每个项目的信息条数
        return info_all

    def save(data):
        # 在循环外部创建连接和游标
        print(len(data))
        connection = pymysql.connect(host='localhost', database='spider', user='root', password='123qwe..')
        cursor = connection.cursor()
        print('连接成功')
        try:
            for i in data:
                print('开始插入数据')
                # 插入数据的 SQL 语句
                sql = """INSERT INTO `spider`.`info_china` 
                        (`name`, `ID`, `num`, `time`, `type`, `local`, `types`, `locals`, `unit`, `message`) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                # 执行插入操作
                if i[8] is not None and i[8] != "":
                    cursor.execute(sql, (i[8], i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[9]))
                    connection.commit()
                    print(f"成功插入 {i[8]} 记录")
                else:
                    print(f"跳过插入，不符合条件")
        except Exception as e:
            print(f"插入数据时发生错误: {e}")
            connection.rollback()  # 回滚事务
        finally:
            cursor.close()  # 关闭游标
            connection.close()  # 关闭连接

if __name__ == '__main__':
    data = info().main()  # main 是它的方法
    info.save(data)  # 直接调用 save 函数