#!/usr/bin/env python
# -*- coding:utf-8 -*-
from spider_book.crawler import get_articles, get_book_list, save_obj, dict_to_json_write_file
import time


if __name__ == '__main__':
    # mo_du = 'https://www.luoxia.com/modu/'
    po_yun = 'https://www.luoxia.com/poyun/'
    tun_hai_url = 'https://www.zhenhunxiaoshuo.com/poyun2tunhai/'
    # 网站类型 2：镇魂
    web_type = 2
    # 获取目录
    contents = get_book_list(tun_hai_url, web_type)
    # 保存目录列表到文件
    contents_file = 'src/tun_hai_book_list'
    save_obj(contents, contents_file)
    dict_to_json_write_file(contents, contents_file)
    print('Get contents done .....\n')

    # chapters = load_json(contents_file)
    # chapters = load_obj(contents_file)
    # print(chapters)

    articles_file = 'src/tun_hai.txt'
    with open(articles_file, "a") as f:
        for key in contents.keys():
            f.write('\n' + key + '\n')
            print('-' * 40 + key + '-' * 40 + '\n')
            paragraphs = get_articles(contents[key], web_type)
            for line in paragraphs:
                f.write(line + '\n')
            print('-' * 40 + 'Write ' + key + 'Done' + '-' * 40 + '\n')
            time.sleep(5)
