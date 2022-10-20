#!/usr/bin/env python
# -*- coding:utf-8 -*-
from openpyxl import Workbook
from openpyxl.styles import Alignment

book = Workbook()
sheet = book.active

sheet.freeze_panes = 'B2'

book.save('freezing.xlsx')