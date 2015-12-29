import os
import re

from core.error import ConfigException
from core.utils import Storage, read_file, xml_parse

config = Storage()
mappers = Storage()


def load_config(config_path):
    """
    加载配置文件，包括数据库的配置文件
    :param config_path:
    :return:
    """
    if not config_path:
        raise ConfigException("配置文件路径不可以为空")
    if not os.path.exists(config_path):
        raise ConfigException("配置文件路径不存在")

    config_content = read_file(config_path)
    pattern = re.compile(r"(<dataSource.*?</dataSource>)", re.S)
    res = re.findall(pattern, config_content)
    data_source = xml_parse(res[0])['dataSource']
    pool = data_source.get('@type', None)
    config.pool_type = pool
    properties = data_source.get('property', None)
    for prop in properties:
        name = prop.get('@name', None)
        value = prop.get('@value', None)
        config[name] = value
    print(config)

    pattern = re.compile(r"(<mapper .*?/>)", re.S)
    mappers = re.findall(pattern, config_content)
    print(mappers)
    for mapper in mappers:
        mp = xml_parse(mapper)
        print(mp)


if __name__ == '__main__':
    base = os.path.dirname(__file__)
    print(base)
    config_path = 'E:/work/projects/pybatis/pybatis-config.xml'
    load_config(config_path)
    # res = xml_parse('\n        <mapper resource="org/mybatis/example/BlogMapper.xml"/>\n')
    # print(res)
    pass
