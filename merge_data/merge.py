# -*- coding:utf-8 -*-
import sys
import csv

# 数据csv文件
data_file = './data.csv'

# tags查找csv文件
find_data_file = './find_data.csv'

# merge结果csv文件
merge_file = './merge.csv'

# 存放tags查找csv字典
find_data = {}

# 最终需要补全的tags数量
tags_total_count = 3

# 表头
header = ['domain']


# 通过click排序并补全tags
def add_tags(item):
    domain = item[0]
    for d in find_data[domain]:
        tag = d['tag']
        if tag not in item:
            item.append(tag)
        if len(item) - 1 == tags_total_count:
            break
    return item


# 读取find_data.csv 到 字典
def read_find_data():
    data1_reader = csv.reader(open(find_data_file, encoding='utf-8'))
    for index, row in enumerate(data1_reader):
        if index == 0:
            continue
        domain = row[0]
        find_data[domain] = []
        del row[0]
        for tag_click in row:
            if tag_click is '':
                continue
            tag = tag_click.strip(':').split(':')[0]
            click_count = int(tag_click.strip(':').split(':')[1])
            find_data[domain].append({'tag': tag, 'count': click_count})
        find_data[domain].sort(key=lambda d: d['count'], reverse=True)


# 生成表头
def set_header():
    for index in range(tags_total_count):
        header.append('tags ' + ('%d' % (index + 1)))
    return header


# 移除list 里tags为空的元素
def remove_empty(data):
    while '' in data:
        data.remove('')
    return data


# merge 数据
def merge_data():
    csv_reader = csv.reader(open(data_file, encoding='utf-8'))
    merge_csv = open(merge_file, 'w', newline='')
    for index, row in enumerate(csv_reader):
        if index == 0:
            row = set_header()
        else:
            row = remove_empty(row)
            tags_count = len(row) - 1
            if tags_count < tags_total_count:
                row = add_tags(row)
        csv_writer = csv.writer(merge_csv, dialect='excel')
        csv_writer.writerow(row)


read_find_data()
merge_data()
