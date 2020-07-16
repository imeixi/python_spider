#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from common.excel_handler import read_excel, write_excel

if __name__ == '__main__':
    filename = os.path.abspath('resource/test.xlsx')
    new_file = os.path.abspath('resource/new.xlsx')
    # read_excel(filename)
    write_excel(new_file)