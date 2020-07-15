#!/usr/bin/env python
# -*- coding:utf-8 -*-
from spider_video.crawler import get_classes_list
from spider_book.crawler import save_obj


if __name__ == '__main__':
    target = 'https://alicache.bdschool.cn/public/bdschool/index/static/ali/w.html?grade=1&_d=2020/06/28'
    # grade_dict = get_classes_tree(target)
    # dict_to_json_write_file(grade_dict, 'classes_tree')
    # class_list = get_classes_list(url=target, grade_max=2, week_max=16)
    class_list = get_classes_list(url=target)
    save_obj(class_list, 'class_list')
