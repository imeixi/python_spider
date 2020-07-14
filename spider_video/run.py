#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from spider_book.crawler import dict_to_json_write_file
import re


def get_video_url(url):
    resp = requests.get(url, verify=False)
    video_url = re.findall(r'videourl="(.*?)\?', resp.text)
    print(video_url)
    return video_url[0]


if __name__ == '__main__':
    target = 'https://alicache.bdschool.cn/public/bdschool/index/static/ali/w.html?grade=1&_d=2020/06/28'
    res = requests.get(url=target, verify=False)

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
                            class_video_url = get_video_url(url)
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
    dict_to_json_write_file(grade_dict, 'classes_tree')
