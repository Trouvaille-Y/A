import os
import datetime


def get_content(fileName, type):
    txt_path = os.getcwd()  # 当前工作路径
    img_path = txt_path
    curr_time = datetime.datetime.now().date()
    if type == 'News':
        txt_path = os.path.join(txt_path, 'Neu ' + str(curr_time), 'News', fileName + '.txt')
        img_path = os.path.join(img_path, 'Neu ' + str(curr_time), 'News', fileName + '.jpg')
        with open(txt_path, 'r+', encoding="utf-8") as file:
            content = file.read()
            content = content.split("\n", 1)  # 分割一次

        if os.path.exists(img_path):
            return content[0], img_path, content[1]
        else:
            return content[0], None, content[1]

    elif type == 'Notice':
        txt_path = os.path.join(txt_path, 'Neu ' + str(curr_time), 'Notice', fileName + '.txt')
    elif type == 'Stu-org':
        txt_path = os.path.join(txt_path, 'Neu ' + str(curr_time), 'Stu-org', fileName + '.txt')

    with open(txt_path, 'r+', encoding="utf-8") as file:
        content = file.read()
        return content
