#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os.path

import requests
from bs4 import BeautifulSoup
import pickle
import json
import time


# 默认格式.pkl
def save_obj(obj, filename):
    with open(filename, 'wb') as fp:
        pickle.dump(obj, fp)


def load_obj(filename):
    with open(filename, 'rb') as fp:
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
    print("ready to get contents ..... ")
    # 默读 主页，获取每章链接
    res = requests.get(url, verify=False)
    print("received a response ..... ")
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
    print("ready to get articles ..... ")
    res = requests.get(url, verify=False)
    print("received a response ..... ")
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


def execute(url, _type, save_path, book_name):
    # 获取目录
    contents = get_book_list(url, _type)
    book_contents_name = book_name + "_contents.txt"
    # 保存目录列表到文件
    # contents_file = '../resource/book/sha_po_lang_list'
    contents_file = os.path.join(save_path, book_contents_name, )
    save_obj(contents, contents_file)
    dict_to_json_write_file(contents, contents_file)
    print('Get contents done .....\n')

    # chapters = load_json(contents_file)
    # chapters = load_obj(contents_file)
    # print(chapters)

    articles_file = os.path.join(save_path, book_name)
    with open(articles_file, "a") as f:
        for key in contents.keys():
            f.write('\n' + key + '\n')
            print('-' * 40 + key + '-' * 40 + '\n')
            paragraphs = get_articles(contents[key], _type)
            for line in paragraphs:
                f.write(line + '\n')
            print('-' * 40 + 'Write ' + key + 'Done' + '-' * 40 + '\n')
            time.sleep(5)

