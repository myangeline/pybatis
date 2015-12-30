import time

from core.mapping import mapping_xml2sql
from core.utils import read_file

__author__ = 'sunshine'

if __name__ == '__main__':
    prev_time = time.time()
    content = read_file('E:\work\projects\pybatis\database.xml')
    res = mapping_xml2sql(content, 'select', 'select_user_by_id', {'age': 20})
    print(res)
    after_time = time.time()
    print(after_time-prev_time)
    pass
