import re

from core.utils import xml_parse

__author__ = 'sunshine'


def mapping_xml2sql(xml, tag, tag_id, kwargs=None):
    m = re.match(r'<mapper\s+namespace\s*=\s*["|\'](.+?)["|\']\s*>', xml)
    if m:
        namespace = m.group(1)
    else:
        namespace = None
    result_type = None
    field_prefix = None
    reg = r'(<%s\s+id=["|\']%s["|\'].*?>(.*?)</%s>)' % (tag, tag_id, tag)
    tag_pattern = re.compile(reg, re.S)
    ids = re.findall(tag_pattern, xml)
    if ids:
        sql_tag, sql_tag_text = ids[0][0], ids[0][1]
        res = xml_parse(sql_tag)
        op_type = res.get(tag)
        result_type = op_type.get('@result_type', None)
        field_prefix = op_type.get('@field_prefix', None)
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
        return sql, params, namespace, result_type, field_prefix
    else:
        return None, [], namespace, result_type, field_prefix


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

