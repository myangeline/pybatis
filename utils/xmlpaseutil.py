import xmltodict

__author__ = 'sunshine'


def xml_parse(xml_doc, encoding='utf-8'):
    return xmltodict.parse(xml_doc, encoding)

