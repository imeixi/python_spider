#!/usr/bin/env python
# -*- coding:utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


def chapter1():
    html = urlopen("http://pythonscraping.com/pages/page1.html")
    print(html.read())


def chapter2():
    url = "http://www.pythonscraping.com/pages/warandpeace.html"
    html = requests.get(url)
    print("html,status code", html.status_code)
    bs_obj = BeautifulSoup(html.text, "lxml")
    name_list = bs_obj.find_all("span", {"class": "green"})
    print(len(name_list))
    for name in name_list:
        print(name.text)


