import os

import xmltodict

__author__ = 'sunshine'


def read_file(name, mode='r', encoding='utf-8'):
    with open(name, mode, encoding=encoding) as handler:
        return handler.read()


def xml_parse(xml_doc, encoding='utf-8'):
    return xmltodict.parse(xml_doc, encoding)


def scan_folder(folder_name):
    files = os.listdir(folder_name)
    return files


def filter_file(name, folder_path):
    return read_file(os.path.join(folder_path, name))

