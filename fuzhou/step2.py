import os

import pandas as pd
from lxml import etree

# 文件夹路径
folder_path = r'f:\\bigdata_data\\caogao'

# 要提取的XPath表达式及其对应的列名
xpath_map = {
    '诉求编号': '/html/body/div/div[5]/div[3]/div/div[1]/div[2]/div',
    '诉求标题': '/html/body/div/div[5]/div[3]/div/div[2]/div[2]/div',
    '诉求内容': '/html/body/div/div[5]/div[3]/div/div[3]/div[2]/div',
    '诉求时间': '/html/body/div/div[5]/div[3]/div/div[4]/div[1]/div[2]/div',
    '事件地点': '/html/body/div/div[5]/div[3]/div/div[4]/div[2]/div[2]/div',
    '回复意见': '/html/body/div/div[5]/div[3]/div/div[6]/div[2]/div/div[1]/text()',
    '回复细节': '/html/body/div/div[5]/div[3]/div/div[6]/div[2]/div/div[2]/text()'
}

# 初始化一个空列表来存储提取的数据
data = []

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)

        # 读取HTML文件
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用lxml解析HTML
        tree = etree.HTML(content)

        # 提取所需元素
        row = {'文件名': filename}
        for column_name, xpath in xpath_map.items():
            elements = tree.xpath(xpath)
            if elements:
                text = elements[0] if isinstance(elements[0], str) else elements[0].text
                if column_name == '诉求时间' and text:
                    # 只保留日期部分
                    text = text.split()[0]
                    row[column_name] = text  # 添加到字典中
                elif column_name == '回复细节' and text:
                    # 拆分“回复细节”列的内容
                    parts = text.split(' 于 ')
                    if len(parts) == 2:
                        reply_unit = parts[0].strip()
                        reply_time = parts[1].split()[0]
                        row['回复单位'] = reply_unit
                        row['回复时间'] = reply_time
                else:
                    row[column_name] = text

        data.append(row)

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 保存为CSV文件
csv_file_path = r'f:\\bigdata_data\\detail_caogao\\data.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8')

print(f"数据已保存到 {csv_file_path}")

