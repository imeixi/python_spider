#!/usr/bin/env python
# -*- coding:utf-8 -*-
from spider_book.crawler import get_articles, get_book_list, save_obj, dict_to_json_write_file
import time


if __name__ == '__main__':
    # mo_du = 'https://www.luoxia.com/modu/'
    po_yun = 'https://www.luoxia.com/poyun/'
    tun_hai_url = 'https://www.zhenhunxiaoshuo.com/poyun2tunhai/'
    can_ci_pin = "https://www.luoxia.com/cancipin/"
    sha_po_lang = "https://www.luoxia.com/shapolang/"
    # 网站类型 1:落霞  2：镇魂
    web_type = 1
    # 获取目录
    contents = get_book_list(sha_po_lang, web_type)
    # 保存目录列表到文件
    contents_file = '../resource/book/sha_po_lang_list'
    save_obj(contents, contents_file)
    dict_to_json_write_file(contents, contents_file)
    print('Get contents done .....\n')

    # chapters = load_json(contents_file)
    # chapters = load_obj(contents_file)
    # print(chapters)

    articles_file = '../resource/book/sha_po_lang.txt'
    with open(articles_file, "a") as f:
        for key in contents.keys():
            f.write('\n' + key + '\n')
            print('-' * 40 + key + '-' * 40 + '\n')
            paragraphs = get_articles(contents[key], web_type)
            for line in paragraphs:
                f.write(line + '\n')
            print('-' * 40 + 'Write ' + key + 'Done' + '-' * 40 + '\n')
            time.sleep(5)
