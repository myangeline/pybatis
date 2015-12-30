import re

from core.utils import xml_parse
from models.user import User

__author__ = 'sunshine'

# 正确的做法应该是，将需要拼接的sql语句使用类似mybatis的形式用xml配置好，这样就比较好了


def mapping_xml2sql(xml, tag, tag_id, kwargs=None):
    m = re.match(r'<mapper\s+namespace\s*=\s*["|\'](.+?)["|\']\s*>', xml)
    if m:
        namespace = m.group(1)
    else:
        namespace = None
    print(namespace)
    # parameter_type = None
    result_type = None
    reg = r'(<%s\s+id=["|\']%s["|\'].*?>(.*?)</%s>)' % (tag, tag_id, tag)
    tag_pattern = re.compile(reg, re.S)
    ids = re.findall(tag_pattern, xml)
    if ids:
        sql_tag, sql_tag_text = ids[0][0], ids[0][1]
        res = xml_parse(sql_tag)
        op_type = res.get(tag)
        # parameter_type = op_type.get("@parameter_type", "HashMap")
        result_type = op_type.get('@result_type', None)
        # 如果有命名空间而且不是字典，则是对象，获取这个对象的属性和值
        if namespace and not isinstance(kwargs, dict):
            kwargs = kwargs.__dict__
        if 'where' in op_type:
            sql_tag_text = re.sub(re.compile(r'<where.*?</where>', re.S), '${where}', sql_tag_text)
            where_text = where_parse(op_type['where'], kwargs)
            sql_tag_text = sql_tag_text.replace("${where}", where_text)
        if 'set' in op_type:
            sql_tag_text = re.sub(re.compile(r'<set.*?</set>', re.S), '${set}', sql_tag_text)
            where_text = set_parse(op_type['set'], kwargs)
            sql_tag_text = sql_tag_text.replace("${set}", where_text)
        p_param = re.compile(r'\${([\w|\d|_]+?)}', re.S)
        # 参数名称
        params = re.findall(p_param, sql_tag_text)
        params = params_filter(kwargs, params)
        sql = re.sub(p_param, '%s', sql_tag_text).replace('\n', '')
        # 格式化sql语句
        sql = re.sub(re.compile(r'\s+'), ' ', sql).strip()
        return sql, params, namespace, result_type
    else:
        return None, [], namespace, result_type


def where_parse(where_text, args):
    # 一条语句中不能有多个<where>标签， 否则会出错
    if_items = where_text.get('if', [])
    prefix = ' '+where_text.get('@prefixOverrides', 'AND')+' '
    where = if_parse(if_items, args)
    sql_where = prefix.join(where)
    return ' where ' + sql_where


def set_parse(set_text, args):
    if_items = set_text.get('if', [])
    prefix = set_text.get('@prefixOverrides', ',')+' '
    sql_set = prefix.join(if_parse(if_items, args))
    return ' set ' + sql_set


def if_parse(if_items, args):
    where = []
    if not isinstance(if_items, list):
        if_items = [if_items]
    for item in if_items:
        test = item.get('@test', None)
        if eval(test, globals(), args):
            text = item.get('#text', None)
            if text:
                where.append(text)
    return where


def params_filter(kwargs, params):
    return [kwargs[param] for param in params]


if __name__ == '__main__':
    xml = """
        <insert id="insertAuthor" parameterType="domain.blog.Author">
            insert into Author (id,username,password,email,bio)
            values (${id},${username},
            ${password},${email},${_bio12}) </insert>
        <update id="updateAuthor" parameterType="domain.blog.Author">
             update Author
                <set prefixOverrides=",">
                    <if test="username is not None">username=${username}</if>
                    <if test="password is not None">password=${password}</if>
                    <if test="email is not None">email=${email}</if>
                </set>
                <where prefixOverrides="AND">
                    <if test="state is not None"> state = ${state}    </if>
                </where>
        </update>
        <delete id="deleteAuthor" parameterType="int">  delete from Author where id = ${id} </delete>
        <select id="selectUsers" parameterType="int" resultType="User">
            select id, username, hashedPassword  from some_table
            <where prefixOverrides="AND">
                <if test="state is not None"> state = ${state}    </if>
                <if test="title is not None"> title like ${title}    </if>
                <if test="author is not None and author.name is not None"> author_name like ${author.name}    </if>
            </where>
            order by id=1
        </select>
    """
    # mapping_xml2sql(xml, 'select', 'selectUsers', {'state': '123', 'title': 'abc', 'author': User()})
    # mapping_xml2sql(xml, 'update', 'updateAuthor', {'id': '2', 'username': 'username', 'password': 'abc',
    #                                                 'email': 'email', 'state': '123'})
    # pattern = re.compile(r'(<insert.*?</insert>|<update.*?</update>|<delete.*?</delete>|<select.*?</select>)', re.S)
    # results = re.findall(pattern, xml)
    # print(results)
    # id_name = 'select'
    # reg = r'(<insert.*?id=["|\']%s["|\'].*?</insert>|<update.*?id=["|\']%s["|\'].*?</update>|' \
    #       r'<delete.*?id=["|\']%s["|\'].*?</delete>|<select.*?id=["|\']%s["|\'].*?</select>)' \
    #       % tuple(['selectUsers' for _ in range(4)])
    # p_id = re.compile(reg, re.S)
    # ids = re.findall(p_id, xml)
    # res = xml_parse(ids[0])
    # print(re.sub(re.compile(r'<where.*?</where>', re.S), '${where}', ids[0]))
    # op_type = res.get(id_name)
    # sql_text = res.get(id_name).get('#text')
    # print(sql_text)

    # 正则筛选sql语句
    # pt = re.compile(r'<%s .*?>(.*?)</%s>' % (id_name, id_name), re.S)
    # sql_og = re.findall(pt, xml)
    # sql_og = sql_og[0]
    # print(sql_og)
    # sql_og_text = re.sub(re.compile(r'<where.*?</where>', re.S), '${where}', sql_og)
    # print(sql_og_text)
    # 参数顺序
    # if 'where' in op_type:
    #     args = {'state': '123', 'title': 'abc', 'author': User()}
    #     where_text = where_parse(op_type['where'], args)
    #     sql_text += where_text
    #     sql_og_text = sql_og_text.replace("${where}", where_text)
    #
    # p_param = re.compile(r'\${([\w|\d|_]+?)}', re.S)
    # 参数名称
    # params = re.findall(p_param, sql_text)
    # 替换关键字成占位符，再根据条件拼接sql语句
    # sql = re.sub(p_param, '%s', sql_text).replace('\n', '')
    # print(sql)
    # sql = re.sub(p_param, '%s', sql_og_text).replace('\n', '')
    # print(sql)
    # 格式化sql语句
    # print(re.sub(re.compile(r'\s+'), ' ', sql).strip())


    # res = xml_parse(xml)
    # print(res)
    # print(User)
    user = User()
    print(user)
    module = User.__module__
    m = __import__(module, globals(), locals(), ['User'])
    print(m)
    u = getattr(m, 'User')
    print(u)
    # print(User.__module__)
    # print(user.__module__)
    # user2 = type('models.user.User', (), {})()
    # print(user2)
    # print(user2())
    # print(user.__dict__)
    # print(user2.__dict__)
    pass
