#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import traceback


def move_file(src_path, dst_path, src_filename, dst_filename=None):
    print('from :', src_path)
    print('to   :', dst_path)
    try:
        f_src = os.path.join(src_path, src_filename)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        if dst_filename:
            f_dst = os.path.join(dst_path, dst_filename)
        else:
            f_dst = os.path.join(dst_path, src_filename)

        shutil.move(src_path, dst_path)
    except Exception as e:
        print('move_file ERROR: ', e)
        traceback.print_exc()
