from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time
import os
from neu_news import write_toFile


def get_stu_org():
    """
    东大先锋网站的学生社团组织
    """
    path = os.getcwd()  # 当前工作路径
    curr_time = datetime.datetime.now().date()
    path = os.path.join(path, 'Neu ' + str(curr_time), 'Stu-org')
    # 如果不存在，则创建路径
    if not os.path.exists(path):
        os.makedirs(path)

    # 解析网页类型
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (XHTML, like Gecko) "
                      "Chrome/79.0.3945.130 Safari/537.36 "
    }

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option,后台运行
    driver = webdriver.Chrome(options=option)

    url = 'http://pioneer.neu.edu.cn/2370/list.htm'
    # 根据网页的特点依次对2370+i操作
    stu_org_name = ""
    for i in range(10):
        res = url.split('/')
        res[3] = str(int(res[3]) + i)
        res = '/'.join(res)
        driver.get(res)
        time.sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')  # 用html5lib解析器，去补全html标签

        div = soup.find('div', {'class': 'wp_articlecontent'})
        subdiv = div.find('div', id='wp_content_w6_0')
        table = subdiv.find('table')
        tbody = table.find('tbody', style='overflow-wrap:break-word;')
        tr_list = tbody.find_all('tr')
        for index, tr in enumerate(tr_list):
            # 提取当前的title信息
            if index == 0:
                name = tr.text
                name = name.replace('/', "或")
                # print(stu_org_name)
                stu_org_name = stu_org_name + str(name) + '\n'

            if index == 1:
                content = tr.text
                write_toFile(path, name, content)
                # print(content)

    with open(path + '.\标题.txt', 'w+') as file:
        file.write(stu_org_name)

    return stu_org_name

