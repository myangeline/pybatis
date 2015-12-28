from utils.xmlpaseutil import xml_parse

__author__ = 'sunshine'


def test_xml_parse():
    doc = '''
        <mapper namespace="org.mybatis.example.BlogMapper">
          <select id="selectBlog" resultType="Blog">
            select * from Blog where id = #{id}
          </select>
        </mapper>
    '''
    js = xml_parse(doc)
    print(js)
    print(js['mapper'])
    print(js['mapper']['@namespace'])
    print(js['mapper']['select'])


if __name__ == '__main__':
    test_xml_parse()
    pass
