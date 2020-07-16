#!/usr/bin/env python
# -*- coding:utf-8 -*-
from spider_book.crawler import load_obj
from concurrent.futures import ThreadPoolExecutor
from common.download import download_file_with_requests_stream
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

    # 初始化线程池
    pool = ThreadPoolExecutor(5)
    class_list = load_obj('class_list')
    for class_content in class_list:
        url = class_content['url']
        if url.split('.')[-1] == 'mp4':
            # 创建视频保存路径和文件
            file_path = os.path.abspath('../resource/class_video') + '/' + str(class_content['grade']) + '/' + class_content['subject']
            file_name = class_content['title'] + '.mp4'
            desc_file_name = class_content['title'] + '.txt'
        else:
            file_path = os.path.abspath('../resource/class_video') + '/' + str(class_content['grade']) + '/' + class_content['subject']
            file_name = url.split('/')[-1]
            desc_file_name = None

        # 如果路径不存在，创建路径
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # 创建视频对应的描述文件
        if class_content['teacher_desc']:
            if desc_file_name:
                with open(os.path.join(file_path, desc_file_name), 'w') as f:
                    f.write(class_content['teacher_desc'] + '\n')
                    if class_content['content_desc']:
                        f.write(class_content['content_desc'])

        pool.submit(download_file_with_requests_stream, url, os.path.join(file_path, file_name))
