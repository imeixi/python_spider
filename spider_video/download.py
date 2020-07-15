#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import spider_video.ProgressBar


def download_file_with_requests(url, filename):
    res = requests.get(url, verify=False)
    with open(filename, "wb") as f:
        f.write(res.content)


# 通过流方式，下载大文件
def download_file_with_requests_stream(url, filename):
    res = requests.get(url, verify=False, stream=True)
    total_length = int(res.headers.get('content-length'))
    # 单次请求最大值
    chunk_size = 1024 * 1024
    progress = spider_video.ProgressBar(filename, total=total_length,
                                        unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
    with open(filename, 'wb') as f:
        for chunk in res.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            progress.refresh(count=len(chunk))


def download_file_with_wget(url, filename):
    print(".........start download " + url + ".......")
    wget.download(url, filename)
    print(".........download end .......")



