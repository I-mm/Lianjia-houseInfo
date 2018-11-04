# -*-coding:utf-8 -*-

import csv

with open('file.csv', 'wb', encoding='UTF-8') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    # 读要转换的txt文件，文件每行各词间以@@@字符分隔
    with open('houseinfo.txt', 'rb') as filein:
        for line in filein:
            line_list = line.split()
            spamwriter.writerow(line_list)
