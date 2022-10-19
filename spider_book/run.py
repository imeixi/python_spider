#!/usr/bin/env python
# -*- coding:utf-8 -*-
from spider_book.crawler import execute
import yaml
import os


if __name__ == '__main__':
    # mo_du = 'https://www.luoxia.com/modu/'
    po_yun = 'https://www.luoxia.com/poyun/'
    tun_hai_url = 'https://www.zhenhunxiaoshuo.com/poyun2tunhai/'
    can_ci_pin = "https://www.luoxia.com/cancipin/"
    sha_po_lang = "https://www.luoxia.com/shapolang/"
    # 网站类型 1:落霞  2：镇魂
    web_type = 1

    # 获取当前脚本所在文件夹路径
    curPath = os.path.dirname(os.path.realpath(__file__))
    # 获取yaml文件路径
    yamlPath = os.path.join(curPath, "bookstore.yaml")

    # 读取配置文件
    with open(yamlPath, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 读取所有配置项
    save_path = config["save_path"]
    all_books = config["all_books"]
    download_all_books = config["download_all_books"]
    custom_books = config["custom_books"]

    # 判断是否下载所有书籍
    if download_all_books:
        book_list = all_books
    else:
        book_list = custom_books

    # 下载图书
    for book_name in book_list:
        url = all_books[book_name]['url']
        _type = all_books[book_name]['_type']
        print("url={}, book name = {}".format(url, book_name))
        execute(url, _type, save_path, book_name)




