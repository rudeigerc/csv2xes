# -*- coding: utf-8 -*-
import logging
import getpass
from xml.etree.ElementTree import Element, SubElement, tostring, Comment, ElementTree
from xml.dom import minidom
import csv
from datetime import datetime


def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml()


def parse_time(time):
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    return datetime.strftime(time.astimezone(), '{}%z'.format(time.isoformat(timespec='milliseconds')))


def parse_csv():
    with open('test.csv', 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, strict=True)
        for row in reader:
            if reader.line_num != 1:
                if not row[0] in instances:
                    instances[row[0]] = [row[1:]]
                else:
                    instances[row[0]].append(row[1:])


def parse_header(root):
    extensions = [
        Element('extension', {
            'name': 'Concept',
            'prefix': 'concept',
            'url': 'http://www.xes-standard.org/concept.xesext'
        }), Element('extension', {
            'name': 'Time',
            'prefix': 'time',
            'url': 'http://www.xes-standard.org/time.xesext'
        }), Element('extension', {
            'name': 'Organizational',
            'prefix': 'org',
            'url': 'http://www.xes-standard.org/org.xesext'
        })
    ]
    classifier = Element('classifier', {'name': 'Activity', 'keys': 'concept:name'})
    strings = [
        Element('string', {'key': 'concept:name', 'value': 'EIS2018-HW1'}),
        Element('string', {'key': 'creator', 'value': username})
    ]

    root.extend(extensions)
    root.append(classifier)
    root.extend(strings)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)
    username = getpass.getuser()
    instances = dict()

    log = Element('log', {'xes.version': '2.0', 'xmlns': 'http://www.xes-standard.org'})
    parse_header(log)
    parse_csv()

    for instance in instances.items():
        trace = SubElement(log, 'trace')
        trace.append(Element('string', {'key': 'concept:name', 'value': instance[0]}))
        for element in instance[1]:
            event = Element('event')
            attrs = [
                Element('string', {'key': 'concept:name', 'value': element[4]}),
                Element('date', {'key': 'time:timestamp', 'value': parse_time(element[1])}),
                Element('string', {'key': 'duration', 'value': element[3]}),
                Element('string', {'key': 'org:resource', 'value': element[5]}),
                Element('string', {'key': 'user_id', 'value': element[0]})
            ]
            event.extend(attrs)
            trace.append(event)

    elementTree = ElementTree(element=log)
    elementTree.write('test.xes', encoding='utf-8', xml_declaration=True)
    # print(prettify(log))
