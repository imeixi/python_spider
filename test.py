#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from common.excel_handler import read_excel

if __name__ == '__main__':
    filename = os.path.abspath('resource/test.xlsx')
    read_excel(filename)