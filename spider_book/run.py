#!/usr/bin/env python
# -*- coding:utf-8 -*-
from spider_book.crawler import get_articles, get_book_list, save_obj, load_obj
import time


if __name__ == '__main__':
    # main_url = 'https://www.luoxia.com/modu/'
    main_url = 'https://www.luoxia.com/poyun/'
    chapters = get_book_list(main_url)
    save_obj(chapters, 'src/po_yun_book_list')
    # dict_to_json_write_file(chapters, 'book_list')
    print('Get chapters done .....\n')

    # chapters = load_json('book_list')
    chapters = load_obj('src/po_yun_book_list')
    print(chapters)

    with open("src/po_yun.txt", "a") as f:
        for key in chapters.keys():
            f.write('\n' + key + '\n')
            print('-' * 40 + key + '-' * 40 + '\n')
            paragraphs = get_articles(chapters[key])
            for line in paragraphs:
                f.write(line + '\n')
            print('-' * 40 + 'Write ' + key + 'Done' + '-' * 40 + '\n')
            time.sleep(5)
