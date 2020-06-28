#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import pickle
import json


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as fp:
        pickle.dump(obj, fp, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as fp:
        return pickle.load(fp)


def dict_to_json_write_file(obj, name):
    with open(name + '.json', 'w') as fj:
        json.dump(obj, fj)
        # fj.write(json.dump(obj))


def load_json(name):
    with open(name + '.json', 'r') as fj:
        return json.loads(fj.read())


def get_book_list(url):
    chapter_dict = dict()
    # 默读 主页，获取每章链接
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'lxml')
    book_list_div = soup.find("div", {"class": "book-list"})
    # book_list_div = soup.find_all("div", class_="stylelistrow")
    list_chapter = book_list_div.findAll('li')
    for chapter in list_chapter:
        try:
            chapter_url = chapter.find('a')['href']
            index = chapter.find('a')['title']
            chapter_dict[index] = chapter_url
            print(index)
        except TypeError:
            index = chapter.find('b')['title']
            chapter_url = chapter.find('b')['onclick'].split('\'')[1]
            chapter_dict[index] = chapter_url
            print(index)

    return chapter_dict


def get_articles(url):
    contents = []
    # 默读 主页，获取每章链接
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'lxml')
    article = soup.find('div', {'id': 'nr1'})
    content_list = article.findAll('p')
    for content in content_list:
        contents.append(content.text)
    return contents


if __name__ == '__main__':
    # main_url = 'https://www.luoxia.com/modu/'
    # chapters = get_book_list(main_url)
    # # save_obj(chapters, 'book_list')
    # dict_to_json_write_file(chapters, 'book_list')
    # print('Get chapters done .....\n')

    # chapters = load_json('book_list')
    chapters = load_obj('book_list')
    print(chapters)

    with open("modu.txt", "a") as f:
        for key in chapters.keys():
            f.write('\n' + key + '\n')
            print('-' * 40 + key + '-' * 40 + '\n')
            paragraphs = get_articles(chapters[key])
            for line in paragraphs:
                f.write(line + '\n')
            print('-' * 40 + 'Write ' + key + 'Done' + '-' * 40 + '\n')
            time.sleep(5)
    email_handler

