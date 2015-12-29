import re

from core.utils import xml_parse
from models.user import User

__author__ = 'sunshine'

# 正确的做法应该是，将需要拼接的sql语句使用类似mybatis的形式用xml配置好，这样就比较好了


class Operator:
    eq = '=='
    ne = '!='
    le = '>'
    lte = '>='
    gt = '<'
    gte = '<='

operator_pattern = re.compile(r'\w+?[eq|ne|le|lte|gt|gte|!=][\w|\d]+?')


def mapping_xml2sql(id):

    pass


def where_parse(where_text, args):
    args = {'state': '123', 'title': 'abc', 'author': User()}
    print('===================where start=================')
    print(where_text)
    if_items = where_text.get('if', [])
    prefix = ' '+where_text.get('@prefixOverrides', 'AND')+' '
    where = []
    for item in if_items:
        print(item)
        test = item.get('@test', None)
        if eval(test, globals(), args):
            text = item.get('#text', None)
            if text:
                where.append(text)
    sql_where = prefix.join(where)
    print(sql_where)
    print('===================where end=================')
    return ' where ' + sql_where


def if_parse(if_text, args):
    pass


if __name__ == '__main__':
    xml = """
        <insert id="insertAuthor" parameterType="domain.blog.Author">
            insert into Author (id,username,password,email,bio)
            values (${id},${username},
            ${password},${email},${_bio12}) </insert>
        <update id="updateAuthor" parameterType="domain.blog.Author">
            update Author set
                username = ${username},
                password = ${password},
                email = ${email},
                bio = ${bio}
            where id = ${id}
        </update>
        <delete id="deleteAuthor" parameterType="int">  delete from Author where id = ${id} </delete>
        <select id="selectUsers" parameterType="int" resultType="User">
        select id, username, hashedPassword  from some_table
         <where prefixOverrides="AND">
            <if test="state is not None"> state = ${state}    </if>
            <if test="title is not None"> title like ${title}    </if>
            <if test="author is not None and author.name is not None"> author_name like ${author.name}    </if>
         </where>
        </select>
    """
    pattern = re.compile(r'(<insert.*?</insert>|<update.*?</update>|<delete.*?</delete>|<select.*?</select>)', re.S)
    results = re.findall(pattern, xml)
    print(results)
    id_name = 'select'
    reg = r'(<insert.*?id=["|\']%s["|\'].*?</insert>|<update.*?id=["|\']%s["|\'].*?</update>|' \
          r'<delete.*?id=["|\']%s["|\'].*?</delete>|<select.*?id=["|\']%s["|\'].*?</select>)' \
          % tuple(['selectUsers' for _ in range(4)])
    print(reg)
    p_id = re.compile(reg, re.S)
    ids = re.findall(p_id, xml)
    print(ids)
    res = xml_parse(ids[0])
    print(res)

    op_type = res.get(id_name)
    sql_text = res.get(id_name).get('#text')
    print(sql_text)
    # 参数顺序
    if 'where' in op_type:
        sql_text += where_parse(op_type['where'])
    p_param = re.compile(r'\${([\w|\d|_]+?)}', re.S)
    # 参数名称
    params = re.findall(p_param, sql_text)
    print(params)
    # 替换关键字成占位符，再根据条件拼接sql语句
    sql = re.sub(p_param, '%s', sql_text).replace('\n', '')
    print(sql)


    # res = xml_parse(xml)
    # print(res)
    # print(User)
    # user = User()
    # print(user)
    # module = User.__module__
    # m = __import__(module, globals(), locals(), ['User'])
    # print(m)
    # u = getattr(m, 'User')
    # print(u)
    # print(User.__module__)
    # print(user.__module__)
    # user2 = type('models.user.User', (), {})()
    # print(user.__dict__)
    # print(user2.__dict__)
    pass
