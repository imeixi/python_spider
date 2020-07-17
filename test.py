#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import openpyxl
from common.excel_handler import read_excel, write_excel, update_excel, stats, filter_sort

if __name__ == '__main__':
    filename = os.path.abspath('resource/test.xlsx')
    # new_file = os.path.abspath('resource/new.xlsx')
    new_file = os.path.abspath('resource/new2.xlsx')
    new_file1 = os.path.abspath('resource/filter_sort.xlsx')
    # read_excel(filename)
    # write_excel(new_file)
    # update_excel(new_file)

    filter_sort(new_file1)
