import json
import os
import re
import time

import requests

now_time = int(time.time())
timeStamp = now_time*1000
count=0
output_dir='f:\\bigdata_data\\caogao'

for i in range(1,15):
    url = 'http://fz12345.fuzhou.gov.cn/jf/event/grid?areacode=350100&starttime=&endtime=&eventstatus=&srctype=&infotype=&evaluate=&keytype=3&keyword=&typeflag=&typedirid=&typeid=&typesmallid=&isn=&queryFineOrSelection=1&page={}&rows=20'.format(i)
    print("这是第{}页".format(i))
    print("============================================")
    headers = {
    "User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }

    response = requests.get(url=url.format(timeStamp), headers=headers)

    # print(response.content.decode('utf-8'),type(response.content.decode('utf-8')))
    content = response.content.decode('utf-8')

    # 需要将content(json.str)--->python对象的(json-dict)
    content_dict = json.loads(content)

    # print(type(content_dict))
    post_list = content_dict['list']
    #print(post_list)

    # #将字典中的每一个dict都迭代出来
    for value_dict in post_list:
        # # #  信件编号billno
        # billno=value_dict['billno']
        # # #     #信件标题case_title
        case_title = value_dict['case_title']
        # # # #     #信件时间incident_time
        # incident_time = value_dict['incident_time'][0:10]
        # # # #     #信件类型-info_type_name
        # info_type_name = value_dict['info_type_name']
        # # #       二级分类type_dirid_name
        # type_dirid_name = value_dict['type_dirid_name']
        # # #       三级分类type_flag_name
        # type_flag_name = value_dict['type_flag_name']
        # #       信件id
        id = value_dict['id']


        # # #     #print看看是否有打印出来
        # print(billno,case_title,incident_time,info_type_name,type_dirid_name,type_flag_name,id)
        # #成功读取网页数据

    #     in_fo_list = [billno,case_title,incident_time,info_type_name,type_dirid_name,type_flag_name,id]
    #     with open('F:/bigdata_data/caogao/fuzhou.csv', 'a', newline='', encoding='utf-8-sig') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(in_fo_list)
    #     #把网页基础数据保存到csv文件
    #
    # print('\n')

        detail_url='http://fz12345.fuzhou.gov.cn/jf/event/getPublicDetail?id={}&areacode=350100'.format(id)
        # print(detail_url)

        detail_response = requests.get(detail_url, headers=headers)
        detail_response.encoding = 'utf-8'  # 确保使用UTF-8编码

        # 提取页面标题作为文件名
        title = value_dict['case_title']
        # print(title)

        filename =f"{title}.html"
        # print(filename)

        # 用下划线或其他有效字符替换无效字符
        sanitized_filename = re.sub(r'[\\/*?:"<>|]', '_', filename)

        filename = os.path.join(output_dir, sanitized_filename)


        # 保存HTML内容到文件夹
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(detail_response.text)

        print(f"Saved {detail_url} to {filename}")

