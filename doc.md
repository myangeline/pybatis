规则：
1. 所有的包含sql语句的xml文件需要放在一个文件夹下，xml文件的名称规则是： 类名小写_mapper.xml，必须以_mapper.xml结尾，为了方便筛选
2. 每个xml映射文件，内容都要使用<mapper>标签作为最外层标签

3. parameter_type:
    用户自定义类名：eg. User
    dict: 字典，键值对的形式

   result_type：
    自定义类名： eg. User, 如果是多条记录，则是数组类型的对象

