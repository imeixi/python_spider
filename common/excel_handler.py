#!/usr/bin/env python
# -*- coding:utf-8 -*-

from openpyxl import load_workbook, Workbook


def read_excel(filename):
    # 默认可读写，若有需要可以指定write_only和read_only为True
    # todo：step 1：打开文件（定只读模式, 性能更好）
    wb = load_workbook(filename, read_only=True)

    # todo：step 2：获取sheet
    # 获取所有sheet名称
    print(wb.sheetnames[])


def write_excel():
    # 指定只写模式, 性能更好
    wb = Workbook(write_only=True)


def update_excel():
    pass

