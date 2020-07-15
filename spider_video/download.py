#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from spider_video.ProgressBar import ProgressBar


def download_file_with_requests(url, filename):
    res = requests.get(url, verify=False)
    with open(filename, "wb") as f:
        f.write(res.content)


# 通过流方式，下载大文件
def download_file_with_requests_stream(url, filename):
    res = requests.get(url, verify=False, stream=True)
    total_length = int(res.headers.get('content-length'))
    print('----- %s -----total_length: %d ---- "开始下载"' % (filename, total_length))
    # 单次请求最大值
    chunk_size = 1024 * 1024
    count = 1
    with open(filename, 'wb') as f:
        for chunk in res.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            pro = len(chunk) * count / total_length * 100
            print('----- %s ----- 已下载 %0.2f %%-----' % (filename, pro))
            count = count + 1
    print('----- %s ----- 下载完毕 ----- ' % filename)


def download_file_with_wget(url, filename):
    print(".........start download " + url + ".......")
    wget.download(url, filename)
    print(".........download end .......")



