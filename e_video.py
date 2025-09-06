import requests
from bs4 import BeautifulSoup
import pymysql
import time
from selenium import webdriver  # 用于控制浏览器
from selenium.webdriver.edge.options import Options     # 用于设置微软浏览器选项
from selenium.webdriver.edge.service import Service     # 用于管理微软浏览器驱动程序
from selenium.webdriver.common.by import By     # 用于定位元素
url  = 'https://www.ihchina.cn/video'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'
}
def op():
    # 创建设置浏览器对象
    q1 = Options()
    # 禁用沙盒模式（增加兼容性）
    q1.add_argument('--no-sandbox')
    # 保持浏览器打开状态，默认是关闭的
    q1.add_experimental_option('detach', True)

    # 创建并启动浏览器
    driver = webdriver.Edge(service=Service(r'Selenium_i\msedgedriver.exe'), options=q1)
    return driver

# 获取视频页面的URL列表
def page_url():
    driver = op()
    # 打开指定网址
    driver.get(url)
    driver.minimize_window()  # 最小化浏览器窗口
    time.sleep(5)
    a = driver.find_element(By.ID, 'look_more')
    a.click()
    time.sleep(5)
    # 等待页面加载完成
    html = driver.page_source  # 获取网页源代码
    soup = BeautifulSoup(html, "html.parser")
    paginator = soup.find("div", id="videotype")
    page_urls = []  # 存储所有页面的URL
    if paginator:
        infos = paginator.find_all("a", href=True)
        for info in infos:
            page_urls.append('https://www.ihchina.cn'+info['href'])
    driver.quit()  # 关闭浏览器        
    return page_urls  # 返回所有页面的URL列表

# 获取视频的URL列表  
def video_url(p):
    url = p  # 获取所有页面的URL列表
    video_urls = {}  # 存储所有视频的URL
    for base_url in url:  # 遍历每个页面的URL
        response = requests.get(base_url, headers=headers)  # 发送GET请求获取页面内容
        if response.status_code == 200:  # 如果请求成功
            soup = BeautifulSoup(response.text, "html.parser")  # 使用BeautifulSoup解析页面内容
            name = soup.find("div", class_="h24").text  # 找到所有的a标签，包含视频的URL
            print(name) # 视频名称
            paginator = soup.find("video")  # 找到包含视频信息的div元素
            if paginator:  # 如果找到了div元素
                infos = paginator.find("source", src=True)  # 找到所有的a标签，包含视频的URL
                print('https://www.ihchina.cn'+infos['src'])    # 视频URL
                video_urls[name]='https://www.ihchina.cn'+infos['src']  # 将视频的URL添加到列表中
    return video_urls  # 返回所有视频的URL列表

# 下载视频
def save_video(v):  
    video_urls = v  # 获取所有视频的URL列表  
    for name, video_url in video_urls.items():  # 遍历每个视频的URL  
        try:  
            # 发送 GET 请求下载视频，设置 stream=True 以分块下载  
            response = requests.get(video_url, headers=headers, stream=True)  
            response.raise_for_status()  # 检查请求是否成功  
            # 将视频内容写入文件，分块写入  
            with open('video//' + name + '.mp4', 'wb') as f:  
                # 设置块的大小，例如8192字节  
                for chunk in response.iter_content(chunk_size=8192):  
                    f.write(chunk)        
            print(f"视频已成功下载到video//{name}.mp4")  
        except requests.exceptions.RequestException as e:  
            print(f"下载视频时发生错误: {e}")  

def save(v):
        for name in v.keys():
            path = 'video//' + name + '.mp4'
            connection = pymysql.connect(host='localhost', database='spider', user='root', password='123qwe..')  
            cursor = connection.cursor()  
            # 插入数据的 SQL 语句  
            sql = """INSERT INTO movie (name, path) VALUES (%s, %s)"""  
            # 执行插入操作  
            cursor.execute(sql,(name,path))  
            connection.commit()  # 提交事务  
            print(f"成功插入 {name} 记录")            
        cursor.close()  # 关闭游标  
        connection.close()  # 关闭连接 

'''print('开始爬取视频页面url')
p = page_url()
print('开始爬取视频url')
v = video_url(p)
print('开始保存数据到数据库')
save(v)
print('开始下载视频')
save_video(v)'''

