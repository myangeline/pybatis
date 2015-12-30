import re

from core.utils import xml_parse, scan_folder, filter_files

__author__ = 'sunshine'


def test_xml_parse():
    doc = '''
        <mapper namespace="org.mybatis.example.BlogMapper">
          <select id="selectBlog" resultType="Blog">
            select * from Blog where id = #{id}
          </select>
        </mapper>
        <mapper namespace="org.mybatis.example.BlogMapper">
          <select id="selectBlog" resultType="Blog">
            select * from Blog where id = #{id}
          </select>
        </mapper>
    '''
    # doc = doc.replace('\r', '').replace('\n', '').strip()
    print(doc)
    pattern = r"(<mapper.*?</mapper>)"
    pattern = re.compile(pattern, re.S)
    mappers = pattern.findall(doc)
    print(mappers)
    for mapper in mappers:
        js = xml_parse(mapper)
        print(js)
        print(js['mapper'])
        print(js['mapper']['@namespace'])
        print(js['mapper']['select'])


def test_scan_folder():
    print(scan_folder('E:\work\projects\pybatis\mappers'))


def test_filter_folder():
    content = filter_files('user', 'E:\work\projects\pybatis\mappers')
    print(content)


if __name__ == '__main__':
    # test_xml_parse()
    # test_scan_folder()
    test_filter_folder()
    pass
