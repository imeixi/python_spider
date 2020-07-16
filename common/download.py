#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib.request
import requests
import wget
from wget import bar_adaptive
import time


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


# python -m wget [options] <URL>
# options:
# -o –output FILE|DIR output filename or directory
def download_file_with_wget(url, filename):
    print(".........start download " + url + ".......")
    wget.download(url, out=filename, bar=bar_adaptive)
    print(".........{0} download end .......".format(filename))
    print(".........{filename} download end .......".format(filename=filename))


# 这里定义的callback用于 urllib 显示下载进度
def callback_download(blocknum, blocksize, totalsize):
    # The reporthook argument should be a callable that accepts
    #      a block number,
    #      a read size, and
    #      the total file size
    # 回调函数
    # @a:已经下载的数据块
    # @b:数据块的大小
    # @c:远程文件的大小
    # '''
    per = 100.0 * blocknum * blocksize / totalsize
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def download_file_with_urllib(url, filename):
    # 这里调用的cbk用于显示下载进度
    urllib.request.urlretrieve(url, filename, reporthook=callback_download)
