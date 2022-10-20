#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os.path

import requests
from bs4 import BeautifulSoup
import pickle
import json
import time
from urllib.parse import urljoin


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


# 获取作者作品
def get_author_books(author_collection, base_url):
    merge_dicts = dict()
    for author in author_collection:
        print(author)
        book_dict = dict()
        print("ready to get books ..... ")
        # 默读 主页，获取每章链接
        url = author_collection[author]
        res = requests.get(url, verify=False)
        print("received a response ..... ")
        soup = BeautifulSoup(res.text, 'lxml')
        # 镇魂 www.zhenhunxiaoshuo.com/
        books_tbody = soup.find('article', {"class": "article-content"})
        books_list = books_tbody.findAll('a')
        for books_info in books_list:
            book_name = None
            book_url = None
            try:
                url_path = books_info['href']
                book_url = urljoin(base_url, url_path)
                print(book_url)
                book_name = books_info.string + '_' + author
                print(book_name)
            except TypeError:
                print(books_info)
            except AttributeError:
                print(books_info)
            if book_name is not None and book_url is not None:
                book_dict[book_name] = book_url
        merge_dicts.update(book_dict)
    print(merge_dicts)
    return merge_dicts


# 获取作品目录 _type 来自网站 1:落霞  2：镇魂
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


# 获取文章内容
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


# 保存文章到本地文件
def execute(url, save_path, book_name, _type):
    # 获取目录
    contents = get_book_list(url, _type)
    print('Get contents done .....\n')
    book_name = book_name + ".txt"
    # 创建小说文件
    articles_file = os.path.join(save_path, book_name)
    with open(articles_file, "a") as f:
        for key in contents.keys():
            f.write('\n' + key + '\n')
            print('-' * 40 + key + '-' * 40 + '\n')
            paragraphs = get_articles(contents[key], _type)
            for line in paragraphs:
                f.write(line + '\n')
            print('-' * 40 + 'Write ' + key + ' Done' + '-' * 40 + '\n')
            time.sleep(8)

