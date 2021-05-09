import sqlite3
import datetime

con = sqlite3.connect('./users.db')  # 打开数据库 没有则创建
cur = con.cursor()  # 获取游标
"""
user表中
name表示其名称   id 唯一标识用户账号 注册时随机生成  password 密码
attribute 表示身份为用户user/管理员admin  state 表示用户是否被加锁 1加锁 0 解锁
question - answer 为密码问题 用于用户忘记密码时找回
"""
# 创建用户表
cur.execute('''CREATE TABLE  IF NOT EXISTS  
              user(
              id INTEGER PRIMARY KEY,
              name VARCHAR(30),
              password CHAR(8),
              attribute VARCHAR(6),
              state INTEGER,
              question VARCHAR(50),
              answer VARCHAR(50))'''
            )  # 调用SQL语句
con.commit()  # 提交

# 创建帖子表
'''
post_id 唯一标识帖子 可以用一个全局变量从1开始分配
label 表示 闲置二手/交友/自习等等
count 评论数  time 发布时间 可以用两者进行排序
uid 发布者id   content title 标题和内容
top  标识该帖子是否置顶
'''
cur.execute('''CREATE TABLE  IF NOT EXISTS  
              post(
              post_id INTEGER PRIMARY KEY,
              label1 TEXT,
              label2 TEXT,
              label3 TEXT,
              count INTEGER,
              time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
              uid INTEGER,
              content TEXT,
              title TEXT,
              top INTEGER,
              FOREIGN KEY(uid) REFERENCES user(id))'''
            )  # 调用SQL语句
con.commit()  # 提交

# 插入时间的方法
# INSERT INTO t2 VALUES (CURRENT_TIMESTAMP);

# 创建评论表
'''
 post_id 帖子id
 rid 回复者id   reply 回复内容
'''
cur.execute('''CREATE TABLE IF NOT EXISTS 
                comment(
                post_id INTEGER,
                rid INTEGER,
                reply TEXT,
                FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
                FOREIGN KEY(rid) REFERENCES user(id) ON DELETE CASCADE
                )''')  # 调用SQL语句
con.commit()  # 提交

# cur.execute('INSERT INTO user(name,id,password,attribute,state,question,answer) VALUES '
#             '("安凯凯",20182369,"akk12345","admin",0,"生日是什么时候","2000-02-14")')
# con.commit()
#
# cur.execute('INSERT INTO user(name,id,password,attribute,state,question,answer) VALUES '
#             '("刘济霆",20182499,"12345678","admin",0,"爱好是什么","套娃")')
# con.commit()
# cur.execute('INSERT INTO user(name,id,password,attribute,state,question,answer) VALUES '
#             '("丁子恒",20181111,"12345678","user",0,"爱好是什么","套娃")')
# con.commit()

cursor = cur.execute('SELECT * from user')
for i in cursor:
    print(i)

# cur.execute('INSERT INTO post(post_id,label1,label2,label3,count,time,uid, content,title,top)'
#             'VALUES (1,"交易",null,null,4,CURRENT_TIMESTAMP,20181111,"有人买吗","出洗发膏",0)')
# con.commit()
#
# cur.execute('INSERT INTO comment(post_id,rid,reply)'
#             'VALUES (1,20182499,"多少钱一瓶")')
# con.commit()

cursor = cur.execute('SELECT * from post')
for i in cursor:
    print(i)

cursor = cur.execute('SELECT * from comment')
for i in cursor:
    print(i)

con.close()
class Connectdb:
    def __init__(self,dbName="./users.db"):
        self.con=sqlite3.connect(dbName)
        self.cur = self.con.cursor()
        self._time_now = "[" + sqlite3.datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]"

    def close_db(self):
        self.cur.close()
        self.conn.close()

    def create_table(self,sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print(self._time_now,"[CREATE TABLE ERROR]",e)
            return False

     def drop_table(self, table_name):
        try:
            self.cur.execute('DROP TABLE {0}'.format(table_name))
            self.conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[DROP TABLE ERROR]", e)
            return False

    def fetchall_table(self, sql, limit_flag=True):
            try:
                self.cur.execute(sql)
                war_msg = self._time_now + ' The [{}] is empty or equal None!'.format(sql)
                if limit_flag is True:
                    r = self._cur.fetchall()
                    return r if len(r) > 0 else war_msg
                elif limit_flag is False:
                    r = self._cur.fetchone()
                    return r if len(r) > 0 else war_msg
            except Exception as e:
                print(self._time_now, "[SELECT TABLE ERROR]", e)

    def insert_update_table(self, sql):
            try:
                self.cur.execute(sql)
                self.conn.commit()
                return True
            except Exception as e:
                print(self._time_now, "[INSERT/UPDATE TABLE ERROR]", e)
                return False

    def insert_table_many(self, sql, value):
            try:
                self.cur.executemany(sql, value)
                self.conn.commit()
                return True
            except Exception as e:
                print(self._time_now, "[INSERT MANY TABLE ERROR]", e)
                return False


