import scrapy
from bs4 import BeautifulSoup
import re
import logging

# 禁用所有日志记录
logging.disable(logging.CRITICAL)
print('spider文件被调用')
class SpiderSpider(scrapy.Spider):
    name = "spider"

    # 自定义构造函数，接受urls和info_all作为参数
    def __init__(self, urls=None, info_all=None, *args, **kwargs):
        super(SpiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls if urls else []
        self.info_all = info_all 

    def start_requests(self):  
        # 遍历URL列表，为每个URL创建Request对象，并指定errback  
        for url in self.start_urls:  
            yield scrapy.Request(url, callback=self.parse, errback=self.handle_error)  

    # 处理请求失败的回调函数  
    def handle_error(self, failure):  
        # 打印错误信息并跳过此URL  
        if failure.value.response:  
            print(f"跳过URL: {failure.value.response.url}, 状态码: {failure.value.response.status}")  
        else:  
            print(f"跳过URL: {failure.request.url}, 错误: {failure.getErrorMessage()}")  

    # 爬取网页
    def parse(self, response):
        print(f"正在爬取URL: {response.url}")
        soup = BeautifulSoup(response.text, "html.parser")
        paginator = soup.find_all("div", class_="x-wrap")[1]  # 找到包含视频信息的div元素
        if paginator:
            try:
                name = re.findall('<div class="h30">(.*?)</div>', str(paginator))[0]  # 找到每个tr中的url
                info = re.findall('<div class="p">(.*?)</div>', str(paginator))
                infos = paginator.find("div", class_="text").text.strip()
                if len(info) < 8:
                    print(f"提取到的数据不足8条, 跳过URL: ")
                info = info[:8]  # 确保只取前8条数据
                info.append(name)
                info.append(infos.replace("\n\t\u3000\u3000", "").replace("\n\u3000\u3000", ""))
                self.info_all.put(info)   
            except Exception as e:  
                self.logger.error(f"Error extracting data from {response.url}: {e}")  

    # 爬虫关闭时的回调函数
    def spider_closed(self, reason):  
        # 爬虫关闭时，这里可以进行收集效果或者清理操作  
        print(f"爬虫关闭: {reason}. 收集数据: {len(self.info_all)} 条.")
