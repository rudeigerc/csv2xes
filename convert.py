# -*- coding: utf-8 -*-
import logging
import getpass
from xml.etree.ElementTree import Element, SubElement, tostring, Comment
from xml.dom import minidom
import csv


def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)
    username = getpass.getuser()

    extensions = [Element('extension', {
        'name': 'Concept',
        'prefix': 'concept',
        'url': 'http://www.xes-standard.org/concept.xesext'
    }), Element('extension', {
        'name': 'Time',
        'prefix': 'time',
        'url': 'http://www.xes-standard.org/time.xesext'
    })]
    classifier = Element('classifier', {'name': 'Activity', 'keys': 'concept:name'})
    strings = [Element('string', {'key': 'concept:name', 'keys': 'EIS2018-HW1'}),
               Element('string', {'key': 'creator', 'keys': username})]

    log = Element('log', {'xes.version': '2.0', 'xmlns': 'http://www.xes-standard.org'})
    log.extend(extensions)
    log.append(classifier)
    log.extend(strings)

    trace = SubElement(log, 'trace')
    trace.append(Element('string', {'key': 'concept:name', 'keys': ''}))

    with open('test.csv', 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, strict=True)
        column = []
        for row in reader:
            if reader.line_num == 1:
                column = row
            else:
                event = Element('event')
                attrs = [
                    Element('string', {'key': 'concept:name', 'value': row[5]})
                ]

    # print(prettify(log))
