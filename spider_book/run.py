#!/usr/bin/env python
# -*- coding:utf-8 -*-
import yaml
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '')))

from spider_book.crawler import execute, get_author_books, dict_to_json_write_file

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
    base_url_zhenhun = config["url"]["zhenhun"]
    save_path = config["save_path"]
    download_way = config["download_way"]
    all_books = config["all_books"]
    custom_books = config["custom_books"]
    author_collection = config["author_collection"]

    # 判断是否下载所有书籍
    if download_way == 1:
        book_list = custom_books
    elif download_way == 2:
        book_list = all_books
    elif download_way == 3:
        book_list = get_author_books(author_collection, base_url_zhenhun)
        author_books = os.path.join(save_path, "author_books", )
        dict_to_json_write_file(book_list, author_books)

    # 下载图书
    for book_name in book_list:
        url = book_list[book_name]
        execute(url, save_path, book_name)
