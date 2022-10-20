#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import copy
import openpyxl


def get_video_url(url):
    resp = requests.get(url, verify=False)
    video_url = re.findall(r'videourl="(.*?)\?', str(resp.text.encode('ISO-8859-1')))[0]
    desc = re.findall(r'<p class="cprofile-content">(.*?)</p>', str(resp.text.encode('ISO-8859-1'), encoding='utf-8'))
    if len(desc) > 1:
        desc_list = str(desc[0]).split('<br/>')
        teacher_desc = desc_list[0].strip()
        try:
            content_desc = desc_list[1].strip()
        except IndexError:
            content_desc = None
    else:
        teacher_desc = None
        content_desc = None
    return video_url, teacher_desc, content_desc


def get_classes_list(url, grade_min=1, grade_max=13, week_min=15, week_max=28):
    # 初始化最终结果list
    classes_list = []
    res = requests.get(url=url, verify=False)
    bf = BeautifulSoup(res.text.encode('ISO-8859-1'), 'lxml')
    # 初始化年级 字典 { x年级： 每周课表字典}
    class_dict = dict()
    # 按年级获取
    for grade_index in range(grade_min, grade_max):
        class_dict['grade'] = grade_index
        print('-' * 40 + str(grade_index) + '年级  开始' + '-' * 40 + '\n')
        # 遍历每周课表的table
        for week_index in range(week_min, week_max):
            print('-' * 40 + str(grade_index) + '年级' + ' 第' + str(week_index) + '周  开始' + '-' * 40 + '\n')
            week_table = bf.find('table', {'grade': grade_index, 'week_index': week_index})
            try:
                day_classes_list = week_table.findAll('tr')
                # 遍历每个tr，获取classes
                for classes in day_classes_list[1:]:
                    day_class_list = classes.findAll('td')
                    for day_index in range(1, len(day_class_list)):
                        class_dict['date'] = day_classes_list[0].findAll('td')[day_index].find('div').text
                        try:
                            # 获取课程标题
                            subject = day_class_list[day_index].find('div', {'class': 'content_table_td_subject'}).text
                            # todo add subject
                            class_dict['subject'] = subject
                            print('subject.......', subject)
                        except AttributeError:
                            print('----------- No Class Subject -----------')

                        # 获取当天所有课程，添加到list
                        class_list_a = day_class_list[day_index].findAll('a')
                        for a_link in class_list_a:
                            # 深度拷贝字典 class_dict
                            class_dict_extend = copy.deepcopy(class_dict)
                            # 每节课的信息
                            url = a_link['href']
                            if str(url).__contains__('weike'):
                                class_video_url, teacher_desc, content_desc = get_video_url(url)
                                class_dict_extend['url'] = class_video_url
                                class_dict_extend['teacher_desc'] = teacher_desc
                                class_dict_extend['content_desc'] = content_desc
                            else:
                                class_dict_extend['url'] = url
                                class_dict_extend['teacher_desc'] = None
                                class_dict_extend['content_desc'] = None
                            title = a_link.find('span', 'conten_table_td_span_title').text
                            class_dict_extend['title'] = title
                            # print('-' * 40 + 'class_dict' + str(class_dict_extend) + '-' * 40 + '\n')
                            classes_list.append(class_dict_extend)
                            # print('-' * 40 + 'classes_list' + str(classes_list) + '-' * 40 + '\n')
            except AttributeError:
                print('----------- NO day_classes_list ------------')
    print('-' * 40 + 'classes_list 汇总结束' + '-' * 40 + '\n')
    return classes_list


def get_classes_tree(url):
    res = requests.get(url=url, verify=False)
    bf = BeautifulSoup(res.text.encode('ISO-8859-1'), 'lxml')
    # 初始化年级 字典 { x年级： 每周课表字典}
    grade_dict = dict()
    # 按年级获取
    for grade in range(1, 13):
        print('-' * 40 + str(grade) + '年级  开始' + '-' * 40 + '\n')
        # 初始化周课表字典 { 第x周：当周课程}
        week_dict = dict()
        # 遍历每周课表的table
        for week_index in range(15, 28):
            print('-' * 40 + str(grade) + '年级' + ' 第' + str(week_index) + '周  开始' + '-' * 40 + '\n')
            # 初始化每天课表
            day_dict = dict()
            week_table = bf.find('table', {'grade': grade, 'week_index': week_index})
            # 获取所有tr
            try:
                day_classes_list = week_table.findAll('tr')
            except AttributeError:
                pass
            # 首个tr是日期，获取所有td [1,6]，是day_dict的 key
            day_key_list = day_classes_list[0].findAll('td')
            for index in range(1, len(day_key_list)):
                key = day_key_list[index].find('div').text
                # 初始化每天字典，key=日期，value=一个list
                day_dict[key] = []

            # 遍历每个tr，获取classes
            for classes in day_classes_list[1:]:
                classes_list = classes.findAll('td')
                for index in range(1, len(classes_list)):
                    key = day_key_list[index].find('div').text
                    # 初始化
                    subject_dict = dict()
                    try:
                        subject = classes_list[index].find('div', {'class': 'content_table_td_subject'}).text
                        # todo add subject
                        subject_dict['subject'] = subject
                        print('subject.......', subject)
                    except AttributeError:
                        pass

                    # 获取当天所有课程，添加到list
                    day_class_list = []
                    class_list_a = classes_list[index].findAll('a')
                    for a_link in class_list_a:
                        # 每节课的信息
                        class_dict = dict()
                        url = a_link['href']
                        if str(url).__contains__('weike'):
                            class_video_url, teacher_desc, content_desc = get_video_url(url)
                        class_dict['url'] = class_video_url
                        title = a_link.find('span', 'conten_table_td_span_title').text
                        class_dict['title'] = title
                        day_class_list.append(class_dict)
                    subject_dict['classes'] = day_class_list
                    day_dict[key].append(subject_dict)
            print('-' * 40 + str(grade) + '年级 ' + ' 第' + str(week_index) + '周 ' + 'day_dict 结束' + '-' * 40 + '\n')
            print(day_dict)
            # week 字典
            week_dict[week_index] = day_dict
        print('-' * 40 + str(grade) + '年级 ' + 'week_dict 汇总 结束' + '-' * 40 + '\n')
        print(week_dict)
        grade_dict[str(grade)] = week_dict
    print('-' * 40 + 'grade_dict 汇总结束' + '-' * 40 + '\n')
    return grade_dict


def convert_list(classes_list):
    convert = []
    first = False
    for class_dict in classes_list:
        if not first:
            convert.append(list(class_dict.keys()))
            first = True
        convert.append(list(class_dict.values()))
    return convert


def convert_excel_2_dict(excel_file):
    video_name_dict = dict()
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active
    # 自动过滤器实际上并不过滤数据，仅用于可视化
    # sheet.auto_filter.add_filter_column(1, [1])
    # sheet.auto_filter.add_filter_column(3, ['语文'])

    # 表头
    # grade, date, subject, url, teacher_desc, content_desc, title
    for row in sheet.rows:
        if row[2].value == '语文':
            key = row[3].value.split('/')[-1]
            video_name_dict[key] = {'grade': row[0].value, 'teacher_desc': row[4].value, 'content_desc': row[5].value,
                                    'title': row[6].value}
    wb.close()
    return video_name_dict
