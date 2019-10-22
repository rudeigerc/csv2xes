# -*- coding: utf-8 -*-
# Author: rudeigerc <rudeigerc@gmail.com>

import csv
import getopt
import logging
import sys


def process(file):
    if file.split('.')[-1] != 'csv':
        logging.error("file format error")
        exit(1)
    data = open('processed.csv', 'w', encoding='utf-8')
    writer = csv.writer(data)
    with open(file, 'r', encoding='utf-8', newline='') as csvfile:
        # GUAHAO_ID | USER_ID | ACTIVITY_START | ACTIVITY_END | DURATION | ACTIVITY | ROLE
        reader = csv.reader(csvfile, strict=True)
        for row in reader:
            if reader.line_num != 1:
                activity = row[5]
                if activity == '首次接诊':
                    activity = '接诊'
                elif activity == '最后一次接诊':
                    continue
                writer.writerow(row[:5] + [activity, row[6]])
            else:
                writer.writerow(row)
    data.close()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                        level=logging.DEBUG)

    if len(sys.argv) == 1:
        logging.error('parameter error')
        exit(1)

    input_file = ''
    opts, args = getopt.getopt(sys.argv[1:], 'hi:')
    for op, value in opts:
        if op == '-i':
            input_file = value
        else:
            exit(1)

    process(input_file)
