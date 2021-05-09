from neu_news import get_news
from stu_org import get_stu_org
from neu_news_interface import get_content
import datetime
import os


# 需要爬取的新闻网页url
news_url_list = ['http://neunews.neu.edu.cn/ddyw/list.htm',  # 东大要闻
                 'http://neunews.neu.edu.cn/tzgg/list.htm'   # 通知公告
                 ]


def crawling_data():
    path = os.getcwd()  # 当前工作路径
    curr_time = datetime.datetime.now().date()
    path = path + "\\Neu " + str(curr_time)
    # print(path)
    if not os.path.exists(path):
        # 得到东大新闻网 东大要闻和通知板块的第一页内容
        print("========================== 东大新闻网 ==========================")
        print("(1)东大要闻：")
        titles = get_news(news_url_list[0])
        print(titles)

        print("(2)通知公告：")
        titles = get_news(news_url_list[1])
        print(titles)

        # 得到东大先锋网关于学生组织的介绍
        print("========================== 东大先锋网 ==========================")
        print("(3)社团介绍：")
        stu_orgNames = get_stu_org()
        print(stu_orgNames)
        print("\n爬取完毕！")
