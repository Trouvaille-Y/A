import sqlite3
import random
import datetime
from neu_news import get_news
from stu_org import get_stu_org
from neu_news_interface import get_content
from crawling import crawling_data
import datetime
import os

class visitor:
    def __init__(self):
        self.pid = []
        self.id = 0  # 账号
        self.name = 0  # 姓名
        self.password = 0  # 密码
        self.attribute = 0  # 身份 admin/user
        self.state = 0  # 是否锁定
        self.question = 0  # 密保问题
        self.answer = 0  # 密码
        self.con = sqlite3.connect('./users.db')  # 打开数据库 没有则创建
        self.cur = self.con.cursor()  # 获取游标

    def log_in(self):  # 系统登录  登录时候可以选择忘记密码
        '''要在这里设置一个忘记密码的按钮，然后调用重置密码 format_password()'''
        while (1):
            print("请输入账号")
            self.id = int(input())  # 界面需要手动输入账号密码
            print("请输入密码")
            self.password = input()
            info = self.cur.execute(
                'SELECT * FROM user WHERE id = ?', (self.id,)).fetchone()
            print(info)
            if not info:  # 不同情况给出提示 并可以多次输入
                print("账号不存在，请重新确认！")
            elif self.password == info[2]:
                self.attribute = info[3]
                self.state = info[4]
                self.question = info[5]
                self.answer = info[6]
                print("登陆成功！")
                return
            else:
                print("密码输入错误，请重新输入！")
                print("是否选择重置密码？1/0")
                x = int(input())
                while not (x == 0 or x == 1):
                    x = int(input())
                if x == 1:
                    self.format_password()

    def register(self):  # 注册
        print("请输入姓名")
        name = input()
        print("请输入密码，密码限制为8位字符")
        password = input()
        print("请再次输入密码")
        password2 = input()
        while password != password2:
            print("两次输入密码不一致，请重新输入")
            print("请输入密码，密码限制为8位字符")
            password = input()
            print("请再次输入密码")
            password2 = input()
        print("请选择你的密保问题")
        l = ["你的生日是什么时候", "你最喜爱的老师是谁", "你最好的小伙伴是谁"]
        print(l)
        print("请选择你的密码问题：1/2/3")
        x = int(input())
        while not 1 <= x <= 3:
            x = int(input())
        print("请输入你的密保问题答案")
        answer = input()
        while answer == "":
            print("密码答案不能为空，请重新输入")
            answer = input()
        id = random.randint(10000000, 99999999)
        # 判断随机生成的id是否已经存在
        while self.cur.execute(
                'SELECT * FROM user WHERE id = ?', (id,)).fetchone():
            id = random.randint(10000000, 99999999)
        print("你注册的账号为" + str(id))
        self.cur.execute('INSERT INTO user(name,id,password,attribute,state,question,answer) VALUES (?,?,?,?,?,?,?)',
                         (name, id, password, "user", 0, l[x - 1], answer))
        self.con.commit()
        print("注册成功！")

    def format_password(self):  # 在忘记密码的时候调用  验证密保并初始化密码为12345678
        print("你将进入重置密码阶段，成功操作后密码将变为12345678")
        info = self.cur.execute(
            'SELECT * FROM user WHERE id = ?', (self.id,)).fetchone()
        print("你的密保问题为：" + info[5])
        print("请输入你的密保问题答案：")
        answer = input()
        while answer != info[6]:
            answer = input()
        self.cur.execute(
            'UPDATE user set password = ? where id = ?', (12345678, self.id,))
        self.con.commit()
        print("重置密码成功！")

    def change_password(self):  # 在忘记密码的时候调用  修改密码
        print("你将进入修改密码阶段")
        info = self.cur.execute(
            'SELECT * FROM user WHERE id = ?', (self.id,)).fetchone()
        print("你的密保问题为：" + info[5])
        print("请输入你的密保问题答案：")
        answer = input()
        while answer != info[6]:
            answer = input()
        print("请输入新密码，密码限制为8位字符")
        password = input()
        print("请再次输入新密码")
        password2 = input()
        while password != password2:
            print("两次输入密码不一致，请重新输入")
            print("请输入密码，密码限制为8位字符")
            password = input()
            print("请再次输入密码")
            password2 = input()
        self.cur.execute(
            'UPDATE user set password = ? where id = ?', (password, self.id,))
        self.con.commit()
        print("修改密码成功！")

    def view_post(self):  # 查看帖子
        global res
        print("选择查看帖子的方式：1.按时间/热度排序 2.按类别排序  3.根据输入内容进行查找")
        k = int(input())
        while not 1 <= k <= 3:
            k = int(input())
        post_actor = post()
        if k == 1:  # 按类别
            res = post_actor.sort_post()
        elif k == 2:  # 按时间或者热度排序
            res = post_actor.select_post()
        else:
            res = post_actor.find_content()
        # res = self.cur.execute('SELECT * from post where label1 = ?',(label[k-1][1],))
        title = []
        for i in res:
            # print(res.fetchone()[-2])
            # print(res.fetchone()[-3])
            self.pid.append(i[0])
            title.append(i[-2])
        print(list(map(lambda x: (title.index(x) + 1, x), title)))


    def browsing_news(self):  # 浏览信息
        print("*")
        path = os.getcwd()  # 当前工作路径
        curr_time = datetime.datetime.now().date()
        path = path + "\\Neu " + str(curr_time) + "\\News" + "\\标题.txt"
        with open(path, 'r+', encoding="gbk") as file:
            content = file.read()
            content = content.split("\n")  # 分割一次
        title = [(content.index(i)+1,i) for i in content]
        title.pop()
        print(title)
        print("请选择你要查看的信息序号")
        k = int(input())
        content1, imgPath, content2 = get_content(title[k-1][1], 'News')
        print("文字段1：")
        print(content1)
        print("\n地址: %s\n" % imgPath)
        print("文字段2：")
        print(content2)

    def club_introduction(self):  # 社团介绍
        path = os.getcwd()  # 当前工作路径
        curr_time = datetime.datetime.now().date()
        path = path + "\\Neu " + str(curr_time) + "\\Stu-org" + "\\标题.txt"
        with open(path, 'r+', encoding="gbk") as file:
            content = file.read()
            content = content.split("\n")  # 分割一次
        title = [(content.index(i) + 1, i) for i in content]
        title.pop()
        print(title)
        print("请输入你要查找的社团介绍")
        k = int(input())
        content = get_content(title[k-1][1], 'Stu-org')
        print(title[k-1][1]+": ")
        print(content)
        print("\n")

    def view_announcement(self):  # 查看公告
        path = os.getcwd()  # 当前工作路径
        curr_time = datetime.datetime.now().date()
        path = path + "\\Neu " + str(curr_time) + "\\Notice" + "\\标题.txt"
        with open(path, 'r+', encoding="gbk") as file:
            content = file.read()
            content = content.split("\n")  # 分割一次
        title = [(content.index(i) + 1, i) for i in content]
        title.pop()
        print(title)
        print("请选择你要查看的公告序号")
        k = int(input())
        content = get_content(title[k-1][1], 'Notice')
        print(title[k-1][1])
        print(content)


class user(visitor):
    def __init__(self, person):
        super().__init__()
        self.pid = person.pid
        self.id = person.id  # 账号
        self.name = person.name  # 姓名
        self.password = person.name  # 密码
        self.attribute = person.attribute  # 身份 admin/user
        self.state = person.state  # 是否锁定
        self.question = person.question  # 密保问题
        self.answer = person.answer  # 密码

    def release_post(self):  # 发布帖子
        global p
        # print(self.attribute)
        # print(self.state)
        if not (self.attribute == "user" and self.state == 0):
            print("非用户账号或账号被锁定")
            return
        print("请输入要发布帖子的标题")
        title = input()
        post_id = random.randint(1, 9999)
        while self.cur.execute(
            'SELECT * from post where post_id = ?',
            (post_id,
             )).fetchone():
            post_id = random.randint(1, 9999)
        # label 这里要进行选择 一级 二级 同时具有多个
        '''''*************************'''
        l1 = ((1, "活动"), (2, "闲聊"), (3, "交友"),
              (4, "自习"), (5, "拼单"), (6, "交易"), (7, "咨询"))
        print("请选择你发布帖子的类别：1 活动 2 闲聊 3 交友 4 自习 5 拼单 6 交易 7 咨询")
        k = int(input())
        while not 1 <= k <= 7:
            k = int(input())
        label1 = l1[k - 1][1]
        label2 = None
        label3 = None
        if k == 1:
            print("请选择你发布帖子的类别：1 院级 2 校级 3 国家级")
            l2 = ((1, "院级"), (2, "校级"), (3, "国家级"))
            p = int(input())
            while p > 3 or p < 1:
                p = int(input())
            label2 = l2[p - 1][1]
        if k == 1 and p == 1:
            print("请输入您的活动类别所属学院")
            label3 = input()
        count = 0
        # time = CURRENT_TIMESTAMP
        uid = self.id
        print("请输入你发布帖子的内容：")
        content = input()
        top = 0
        self.cur.execute(
            'INSERT INTO post(post_id,label1,label2,label3,count,uid,content,title,top) VALUES '
            '(?,?,?,?,?,?,?,?,?)',
            (post_id,
             label1,
             label2,
             label3,
             count,
             uid,
             content,
             title,
             top))
        self.con.commit()

    #  自动继承父类的查看帖子函数
    def reply_post(self):  # 回复帖子
        if not (self.attribute == 'user' and self.state == 0):
            print("非用户账号或账号被锁定")
            return
        self.view_post()
        print("选择你要回复的帖子的编号")
        m = int(input())
        if m > len(self.pid) or m < 1:
            print("请重新输入要回复的帖子的编号")
            m = int(input())
        post_id = self.pid[m - 1]
        self.cur.execute(
            'UPDATE post set count = count + 1 where post_id = ?', (post_id,))
        self.con.commit()
        print("请输入要回复的内容")
        reply = input()
        rid = self.id
        self.cur.execute(
            'INSERT INTO comment(post_id,rid,reply) VALUES (?,?,?)', (post_id, rid, reply))
        self.con.commit()


class administrator(visitor):
    def __init__(self, person):
        super().__init__()
        self.pid = person.pid
        self.id = person.id  # 账号
        self.name = person.name  # 姓名
        self.password = person.name  # 密码
        self.attribute = person.attribute  # 身份 admin/user
        self.state = person.state  # 是否锁定
        self.question = person.question  # 密保问题
        self.answer = person.answer  # 密码

    def release_announcement(self):  # 发布公告
        if not (self.attribute == "admin"):
            print("非管理员账号")
            return
        print("请输入要发布公告的标题")
        title = input()
        post_id = random.randint(1, 9999)
        while self.cur.execute(
            'SELECT * from post where post_id = ?',
            (post_id,
             )).fetchone():
            post_id = random.randint(1, 9999)
        count = 0
        uid = self.id
        print("请输入你发布公告的内容：")
        content = input()
        top = 0
        self.cur.execute(
            'INSERT INTO post(post_id,label1,label2,label3,count,uid,content,title,top) VALUES '
            '(?,?,?,?,?,?,?,?,?)', (post_id, "公告", None, None, count, uid, content, title, top))
        self.con.commit()

    def top_post(self):  # 置顶帖子
        a = self.search_post()
        print(a)
        pid = int(input("请输入您要置顶的帖子ID"))
        conn = sqlite3.connect('users.db')
        print("open successfully")
        db = conn.cursor()
        p1 = db.fetchone()
        db.execute('UPDATE post set top = 1 where post_id=?', (pid,))
        conn.commit()
        print(p1)

    # # 管理用户包含搜索、锁定、解锁
    # def search(self):  # 搜索
    #     n = int(input("搜索用户（1），搜索贴子（2），返回（0）"))
    #     if n == 1:
    #         self.search_user()
    #     elif n == 2:
    #         self.search_post()
    #     else:
    #         return

    def search_user(self):
        '''
        userid = int(input("输入用户id"))
        conn = sqlite3.connect('users.db')
        print("open successfully")
        db = conn.cursor()
        db.execute('SELECT * FROM user WHERE id=?', (userid,))
        conn.commit()
        a = db.fetchone()
        print(a)
        conn.close()
        '''
        sql = self.cur.execute(
            'SELECT id from user where attribute = ?', ("user",))
        res = sql.fetchall()
        id = [(res.index(i) + 1, res[0]) for i in res]
        print(id)

    def search_post(self):
        '''
        sql = self.cur.execute("SELECT id from user where attribute = ?",("user",))
        res = sql.fetchall()
        id = [(res.index(i)+1,res[0]) for i in res]
        print("请输入要锁定的用户id的编号")
        print(k)
        userid = id[k-1][1]
        '''
        self.search_user()
        print("可以选择输入查找帖子的用户id")
        userid = input()
        if userid:
            userid = int(userid)
        content = input("输入贴子内容（部分）")
        conn = sqlite3.connect('users.db')
        db = conn.cursor()
        db.execute(
            'SELECT * FROM post WHERE content like ? or uid = ?',
            ('%' +
             content +
             '%',
             userid,
             ))
        conn.commit()
        a = db.fetchmany()
        conn.close()
        return a

    def delete_post(self):  # 删除帖子
        a = self.search_post()
        print(a)
        pid = input("请输入您要删除的帖子ID")
        if pid == "":
            return
        pid = int(pid)
        conn = sqlite3.connect('users.db')
        db = conn.cursor()
        db.execute('DELETE from post where post_id=?', (pid,))
        conn.commit()
        p1 = db.fetchone()
        print(p1)
        print("删除成功！")

    def lock_user(self):  # 锁定用户
        self.search_user()
        userid = input("请输入用户id")  # 输入用户id
        while userid == "":
            userid = input("请输入用户id")  # 输入用户id
        userid = int(userid)
        while not self.cur.execute('SELECT * FROM user WHERE id=?', (userid,)):
            userid = int(input("请输入用户id"))

        m = self.cur.execute(
            'SELECT * FROM user WHERE id=?', (userid,)).fetchone()
        if m[4] == 1:
            print("当前用户已经处于锁定状态")
            # print("即将返回主菜单")
        else:
            print("是否将该用户锁定？")
            n = int(input("0 锁定；1 取消"))
            if n != (0 or 1):
                n = int(input("0 锁定；1 取消"))
            if n == 0:
                sql = 'update user set state=1 where id=?'
                self.cur.execute(sql, (userid,))
                self.con.commit()
                print("已将该用户锁定")
            if n == 1:
                return

    def unlock_user(self):  # 解锁用户
        self.search_user()
        userid = input("请输入用户id")  # 输入用户id
        while userid == "":
            userid = input("请输入用户id")  # 输入用户id
        userid = int(userid)
        while not self.cur.execute('SELECT * FROM user WHERE id=?', (userid,)):
            userid = int(input("请输入用户id"))
        m = self.cur.execute(
            'SELECT * FROM user WHERE id=?', (userid,)).fetchone()
        if m[4] == 0:
            print("当前用户未被锁定")
        else:
            print("是否将该用户解锁？")
            n = int(input("0 解锁；1 取消"))
            if n != (0 or 1):
                n = int(input("0 解锁；1 取消"))
            if n == 0:
                sql = 'update user set state=0 where id=?'
                self.cur.execute(sql, (userid,))
                self.con.commit()
                print("已将该用户解锁")
                # print("即将返回主菜单")
            if n == 1:
                return


class post():
    def __init__(self):
        self.con = sqlite3.connect('./users.db')  # 打开数据库 没有则创建
        self.cur = self.con.cursor()  # 获取游标

    def sort_post(self):  # 排序帖子
        global res
        print('请选择排序方式')
        num = int(input('0 最新发布；1 最高热度'))
        if num == 0:
            sql = 'select * from post order by time desc'
            res = self.cur.execute(sql)
            self.con.commit()
        if num == 1:
            sql = 'select * from post order by count desc'
            res = self.cur.execute(sql)
            self.con.commit()
        return res

    def select_post(self):  # 筛选帖子
        print('请选择筛选方式')
        label = ((1, "活动"), (2, "闲聊"), (3, "交友"), (4, "自习"),
                 (5, "拼单"), (6, "交易"), (7, "咨询"), (8, "公告"))
        print("请选择你发布帖子的类别：1 活动 2 闲聊 3 交友 4 自习 5 拼单 6 交易 7 咨询 8 公告")
        k = int(input())
        while not 1 <= k <= 8:
            k = int(input())
        tag = label[k - 1][1]
        sql = "select * from post where label1=?"
        res1 = self.cur.execute(sql, (tag,))
        return res1

    def find_content(self):
        print("请选择输入要查找帖子的标题或内容")
        content = input("输入贴子标题/内容（部分）")
        sql = 'SELECT * FROM post WHERE content like ? or title like ?'
        res2 = self.cur.execute(
            sql, ('%' + content + '%', '%' + content + '%',))
        return res2


if __name__ == "__main__":
    # crawling_data()
    person = visitor()
    person.browsing_news()
    person.view_announcement()
    person.club_introduction()
    '''
    person.log_in()
    if person.attribute == "user":
        p = user(person)
        p.view_post()
        # p.release_post()
        # person.view_post()
        # p.reply_post()
    elif person.attribute == "admin":
        p = adminstrator(person)
        # p.top_post()
        p.delete_post()
        # p.lock_user()
        p.unlock_user()
    '''