#!/usr/bin/env python
# -*- coding:utf-8 -*-

from spider_video.download import download_file_with_requests_stream

if __name__ == '__main__':
    url = 'https://alivcache.bdschool.cn/vd/6548fc2cb9bf542376b8953219c70730.mp4'
    download_file_with_requests_stream(url, '1.mp4')
