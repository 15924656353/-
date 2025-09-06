import pandas as pd  
import pymysql  
import matplotlib.pyplot as plt  

# 配置 matplotlib 使用中文字体  
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体  
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题 

# 连接到 MySQL 数据库  
connection = pymysql.connect(  
    host='localhost',  
    user='root',  
    password='123qwe..',  
    database='spider',  
    charset='utf8mb4'  
)  

# 使用 SQL 查询获取数据  
query = "SELECT type, local, COUNT(*) as count FROM info_china GROUP BY type, local"  
df = pd.read_sql(query, connection)  

# 关闭数据库连接  
connection.close()  
print(len(df))
# 删除 category 列的前三个字符  
df['type'] = df['type'].str[3:] 
df['local'] = df['local'].str[5:]


# 根据类别绘制饼图  
def plot_pie_chart(df):  
    category_counts = df.groupby('type')['count'].sum()  
    
    plt.figure(figsize=(8, 6))  
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')  
    plt.title('类别分布饼图')  
    plt.axis('equal')  # 使饼图为圆形  
    plt.show()  

# plot_pie_chart(df)  

# 根据省份绘制柱状图  
def plot_bar_chart(df):  
    province_counts = df.groupby('local')['count'].sum()  
    
    plt.figure(figsize=(15, 6))  
    province_counts.plot(kind='bar', color='skyblue')  
    plt.title('各省份数量柱状图')  
    plt.ylabel('数量')  
    plt.xlabel('省份')  
    plt.xticks(rotation=45)  
    plt.tight_layout()  
    plt.show()  

plot_bar_chart(df)    