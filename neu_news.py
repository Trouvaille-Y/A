from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
import datetime
import time
import os
import requests


def write_toFile(path, title, content):
    title = title + '.txt'
    filename = os.path.join(path, title)
    with open(filename, 'w+', encoding="utf-8") as f:
        f.write(content)


def get_news(url):
    """
    获取网页html
    """
    pattern = re.compile(r'.*/(.+)/.*', re.M | re.I)
    type = pattern.match(str(url)).group(1)
    work_path = os.getcwd()  # 当前工作路径
    curr_time = datetime.datetime.now().date()
    if type == 'ddyw':
        work_path = os.path.join(work_path, 'Neu ' + str(curr_time), 'News')
    elif type == 'tzgg':
        work_path = os.path.join(work_path, 'Neu ' + str(curr_time), 'Notice')
    # 如果不存在，则创建路径
    if not os.path.exists(work_path):
        os.makedirs(work_path)

    # 解析网页类型
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (XHTML, like Gecko) "
                      "Chrome/79.0.3945.130 Safari/537.36 "
    }

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 设置option,后台运行
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')  # 用html5lib解析器，去补全html标签

    news_title = ""
    ul = soup.find('ul', {'class': 'news_list clearfix'})
    li_list = ul.find_all('li')
    res_list = driver.find_elements_by_xpath("//div[@class='column-news-list clearfix']"
                                             "/ul[@class='news_list clearfix']/li"
                                             "/span[@class='news_title']")  # 找到位置
    for index, li in enumerate(li_list):
        # 提取当前的title信息
        pattern = re.compile(r'<.*> <.*> <.*>(.+)</a> </span> <.*>(.+)</span> </li>', re.M | re.I)
        res = pattern.match(str(li))
        title = res.group(1)
        if type == 'tzgg':
            title = title + res.group(2)
        title = title.replace('/', "或")
        # print(title)
        news_title = news_title + str(title) + '\n'
        # news_title = list(filter(None, news_title))

        # 提取具体的新闻网页内容
        action = ActionChains(driver)
        action.move_to_element(res_list[index])  # 移动至点击元素上
        time.sleep(1)
        action.click().perform()  # 设置点击动作
        time.sleep(1)
        current_window = driver.current_window_handle  # 获取所有页面句柄
        # 跳转页面
        all_Handles = driver.window_handles
        # 如果新的pay_window句柄不是当前句柄，用switch_to_window方法切换
        for window in all_Handles:
            if window != current_window:
                driver.switch_to.window(window)
                time.sleep(1)

        # 爬取内容
        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')  # 用html5lib解析器，去补全html标签
        article = soup.find('article', {'class': 'read article_content'})
        div_subclass = article.find('div', {'class': 'wp_articlecontent'})
        plist = div_subclass.find_all('p')  # 找到位置

        content = ""
        for p in plist:
            if p.text and p.text[0] != '<':
                content = content + p.text + '\n'

        img = div_subclass.find('img')  # 图片
        img_urlBase = 'http://neunews.neu.edu.cn'
        if img:
            img_src = img_urlBase + img["src"]
            image = requests.get(img_src, headers=header)  # 下载图片
            imgName = os.path.join(work_path, title + '.jpg')
            with open(imgName, 'wb') as file:  # 保存图片
                file.write(image.content)

        # 保存文件
        write_toFile(work_path, title, content)
        # print(content)

        # 跳转回原界面
        driver.close()
        driver.switch_to.window(current_window)
        time.sleep(2)

    # 保存标题文件
    with open(work_path + '\\标题.txt', 'w+') as file:
        file.write(news_title)

    return news_title

