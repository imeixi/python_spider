#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
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


# _type 来自网站 1:落霞  2：镇魂
def get_book_list(url, _type):
    chapter_dict = dict()
    # 默读 主页，获取每章链接
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'lxml')
    # book_list_div = soup.find_all("div", class_="stylelistrow")
    if 1 == _type:
        # 落霞 www.luoxia.com
        book_list_div = soup.find("div", {"class": "book-list"})
        list_chapter = book_list_div.findAll('li')
    elif 2 == _type:
        # 镇魂 www.zhenhunxiaoshuo.com/
        book_list_div = soup.find("div", {"class": "excerpts"})
        list_chapter = book_list_div.findAll('article')
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


def get_articles(url, _type):
    contents = []
    # 默读 主页，获取每章链接
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'lxml')
    if 1 == _type:
        # 落霞 www.luoxia.com
        article = soup.find('div', {'id': 'nr1'})
    elif 2 == _type:
        # 镇魂 www.zhenhunxiaoshuo.com/
        article = soup.find('article', {'class': 'article-content'})
    content_list = article.findAll('p')
    for content in content_list:
        contents.append(content.text)
    return contents

