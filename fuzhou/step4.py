from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

# 读取CSV文件，指定诉求时间和回复时间为日期时间类型
csv_file_path = r'f:\\bigdata_data\\detail_caogao\\data.csv'
df = pd.read_csv(csv_file_path, parse_dates=['诉求时间', '回复时间'])

# 计算处理时间差值
df['处理时间'] = (df['回复时间'] - df['诉求时间']).dt.total_seconds() / (60 * 60 * 24)  # 转换为天数

# 处理时间差值直方图，显示每个直方上的数字
plt.figure(figsize=(10, 6))
plt.hist(df['处理时间'], bins=20, edgecolor='black', alpha=0.7)
plt.xlabel('处理时间差值（天）')
plt.ylabel('频数')
plt.title('事件处理时间的差值直方图')
plt.grid(True)

# 显示每个直方上的数字
for i, v in enumerate(df['处理时间'].value_counts().sort_index()):
    plt.text(i + 0.5, v + 5, str(v), ha='center', va='bottom', fontsize=8)

# 解决中文乱码问题，设置字体为SimHei或者其他支持的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

plt.show()

# 提取年份和月份列
df['年份'] = df['诉求时间'].dt.year
df['月份'] = df['诉求时间'].dt.month

# 2023年每个月处理事件数量扇形图
events_2023 = df[df['年份'] == 2023].groupby('月份').size()
month_labels = [datetime.strptime(str(month), '%m').strftime('%B') for month in events_2023.index]
plt.figure(figsize=(8, 8))
plt.pie(events_2023, labels=month_labels, autopct='%1.1f%%', startangle=140)
plt.title('2023年每个月处理事件数量扇形图')
plt.show()

# 2023和2024年处理事件数量对比直方图
events_2023_2024 = df['年份'].value_counts().sort_index()
plt.figure(figsize=(8, 6))
events_2023_2024.plot(kind='bar', color=['blue', 'green'], alpha=0.7)
plt.xlabel('年份')
plt.ylabel('事件数量')
plt.title('2023和2024年处理事件数量对比直方图')

# 显示每个直方上的数字
for i, v in enumerate(events_2023_2024):
    plt.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=8)

plt.xticks(rotation=0)
plt.grid(axis='y')
plt.show()

# 绘制包含特定关键词的诉求标题数目柱状图
keywords = ['公积金', '医保', '小学', '电动车']
keyword_counts = [df[df['诉求标题'].str.contains(keyword)].shape[0] for keyword in keywords]

plt.figure(figsize=(8, 6))
bars = plt.bar(keywords, keyword_counts, color='skyblue')

# 显示每个柱状图上的数字
for bar in bars:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(int(bar.get_height())),
             ha='center', va='bottom', fontsize=10)

plt.xlabel('关键词')
plt.ylabel('出现次数')
plt.title('诉求标题中关键词出现次数')
plt.grid(axis='y')
plt.show()
