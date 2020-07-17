#!/usr/bin/env python
# -*- coding:utf-8 -*-
from spider_book.crawler import load_obj
from spider_video.crawler import convert_list, convert_excel_2_dict
from common.excel_handler import write_list_2_excel
import os


if __name__ == '__main__':
    # target = 'https://alicache.bdschool.cn/public/bdschool/index/static/ali/w.html?grade=1&_d=2020/06/28'
    # 获取class_tree
    # grade_dict = get_classes_tree(target)
    # dict_to_json_write_file(grade_dict, 'classes_tree')

    # 获取class_tree
    # class_list = get_classes_list(url=target, grade_max=2, week_max=16)
    # class_list = get_classes_list(url=target)
    # save_obj(class_list, 'class_list')

    file_path = os.path.abspath('../resource/video/class_list.pkl')
    class_list = load_obj(file_path)
    class_list_2_excel = convert_list(class_list)

    # 下载视频
    dir_path = os.path.abspath('../resource/class_video')
    # download_file(dir_path, class_list)

    filename = os.path.join(dir_path, 'classes_info.xlsx')
    print(filename)
    # write_list_2_excel(filename, class_list_2_excel)

    # 重命名文件
    # step 1：video name 作为字典key， {grade, teacher_desc, content_desc, title}字典为value
    video_name_dict = convert_excel_2_dict(filename)
    # step 2：遍历文件夹，批量重命名文件
    os.walk()

