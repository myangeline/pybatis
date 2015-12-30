import pymysql
from DBUtils.PooledDB import PooledDB

from core.mapping import mapping_xml2sql
from core.utils import filter_file
from models.user import User

__author__ = 'sunshine'


class CreateConnectPool:
    """
    创建连接池类
    """

    def __init__(self, folder, creator, min_cached=0, max_cached=0, max_shared=0, max_connections=0, blocking=False,
                 max_usage=None, set_session=None, reset=True, failures=None, ping=1, *args, **kwargs):
        # xml映射文件所在的文件夹
        self.folder = folder
        self.pool = PooledDB(creator, mincached=min_cached, maxcached=max_cached,
                             maxshared=max_shared, maxconnections=max_connections, blocking=blocking,
                             maxusage=max_usage, setsession=set_session, reset=reset,
                             failures=failures, ping=ping, *args, **kwargs)
        # 定义允许的操作类型
        self.crud = ['select', 'insert', 'update', 'delete']

    def get_pool(self):
        """
        获取连接池对象
        :return:
        """
        return self.pool

    def get_connect(self):
        """
        从连接池中获取一个连接
        :return:
        """
        return self.pool.connection()

    @staticmethod
    def close_connect(conn):
        """
        关闭连接
        :param conn:
        :return:
        """
        conn.close()

    def filter_crud(self, crud):
        return crud in self.crud

    def execute_sql(self, mapper_name, crud, crud_id, kwargs=None, fetchone=True):
        """
        执行sql语句
        :param mapper_name: 映射sql的xml文件名称
        :param crud: 数据库 select update insert delete操作，也是xml的标签名
        :param crud_id: 标签的id
        :param kwargs: 参数
        :param fetchone: select操作时候获取的结果集
        :return:
        """
        if self.filter_crud(crud):
            # 可以考虑初始化的时候一次全部读入内存，就是不知道会不会有问题
            xml = filter_file(mapper_name, self.folder)
            sql, args, namespace, result_type = mapping_xml2sql(xml, crud, crud_id, kwargs)
            print(sql, args, namespace, result_type)
            # 如果 namespace, result_type都不是空，则是映射成指定对象
            module = __import__(namespace, globals(), locals(), [result_type])
            cls = getattr(module, result_type)
            print(cls)
            args = [str(arg) for arg in args]
            print(args)
            if sql:
                if crud == 'select':
                    return self.execute_select(sql, args, cls, fetchone)
                else:
                    return self.execute_update(sql, args)
            else:
                return None

    def execute_select(self, sql, args=None, cls=None, fetchone=True):
        """
        执行查询语句
        :param sql:
        :param args:
        :param cls:
        :param fetchone:
        :return:
        """
        if args is None:
            args = []
        conn = self.get_connect()
        cursor = conn.cursor()
        # todo 在使用了DBUtils以后，所获取的到连接都不是pymysql原来的conn, 在执行的时候没有进行参数检查，很可能存在 sql injection
        # todo 原来使用动态参数绑定就可以了
        cursor.execute(sql, args)
        if cls is None:
            res = cursor.fetchone() if fetchone else cursor.fetchall()
        else:
            if fetchone:
                item = cursor.fetchone()
                if item:
                    res = cls()
                    for k, v in item.items():
                        setattr(res, k, v)
                else:
                    res = None
            else:
                items = cursor.fetchall()
                res = []
                for item in items:
                    c = cls()
                    for k, v in item.items():
                        setattr(c, k, v)
                    res.append(c)
        cursor.close()
        conn.close()
        return res

    def execute_update(self, sql, args):
        """
        执行 更新，删除，插入语句
        :param sql:
        :param args:
        :return: 返回操作影响的行数
        """
        if args is None:
            args = []
        conn = self.get_connect()
        cursor = conn.cursor()
        rows = cursor.execute(sql, args)
        cursor.close()
        conn.close()
        return rows

if __name__ == '__main__':
    pool = CreateConnectPool(
            'E:\work\projects\pybatis\mappers',
            pymysql, 5,
            host='192.168.0.62',
            port=3306,
            user='root',
            passwd='53iq.com',
            db='ebdb_smartsys',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
    res = pool.execute_sql('user_mapper.xml', 'select', 'select_user_by_id', {'user_account': 1})
    print(res.__dict__)
    # user = User()
    # res = pool.execute_sql('user_mapper.xml', 'select', 'select_user_by_id', user, False)
    print(res)
    # conn = pool.get_connect()
    # cur = conn.cursor()
    # cur.execute("select * from ebt_user where ebf_user_id='1'")
    # res = cur.fetchone()
    # print(res)
    # cur.close()
    # conn.close()
    pass
