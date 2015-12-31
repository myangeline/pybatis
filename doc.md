# pybatis使用文档

## 1. 期望的目标
原来每次使用多表查询的时候都需要根据条件去筛选，也就需要去根据条件拼接sql语句，有点烦，每次都要拼很久，还害怕拼错，所以就借鉴java中的MyBatis,使用
xml预先写好，条件也设定好，根据传来的参数去自动判断哪些字段需要拼接，主要还是where的问题

## 2. xml文档规则
由于没有写一个DTD来限制，所以主要靠自己检查了，如果写错了可能就没结果啦...

1. 所有的包含sql语句的xml文件需要放在一个文件夹下，xml文件的名称规则是： 类名小写_mapper.xml，必须以_mapper.xml结尾，为了方便筛选

2. 每个xml映射文件的内容都要使用<mapper>标签作为最外层标签，而且只能有一个<mapper>标签，<mapper>中有`namespace`属性，用于标记下面用到的类所属的模块

3. <mapper>中可以使用的标签有 <select>, <insert>, <update>, <delete>四个，主要还是增删改查的操作。<select>中有 `id`, `parameter_type`,
`result_type`, `field_prefix` 属性，其中 `id` 是必须的，其他不是必须。
    
  *id：在整个xml中需要唯一，这个是唯一标识sql语句的，否则查找不到
  *parameter_type：参数的类型，可以是类名，如果不是类的话就直接为空，就是不写就好了，其实这个属性可以不写，如果是类的话，参数直接传一个类名即可，否则需要字典（dict）
  *result_type：结果类型，可以为空，如果结果需要封装成类的话，写上类名即可
  *field_prefix：字段的前缀，这个有点取巧，数据库字段和类属性不一致时候，如果属性只是和数据库字段只差一个前缀的话，那么些在这里即可，如果很乱，没有规则的话，那就取不到值
 
4. 标签下面就是sql语句，语句中可以插入<where>和<set>标签, <where>,<set>标签中都有属性 `prefixOverrides`，<set> 中可以不写属性，默认为 `,`, <where>中属性不写默认是 `AND`, 还可以取 `OR`,
    用于拼接 where的条件连接和set的条件连接
    
5. <where>和<set>标签下都是<if>标签，<if>标签中有 `test` 属性，内容是一个表达式，也是sql语句的一部分。如果属性中的条件成立的话，
那么sql就会拼接上<if>标签中的内容

6. sql语句中的所有参数都用 `${param_name}` 的形式写

## 3. xml文档示例

    <mapper namespace="models.user">
        <select id="select_user_by_id" parameter_type="User" result_type="User" field_prefix="ebf_">
            select * from ebt_user where ebf_user_account=${user_account}
        </select>
        
        <select id="abc">
            select * from tb_user
            <where prefixOverrides="AND">
                <if test="age>10"> age = ${age}</if>
            </where>
            order by id
        </select>
        
        <update id="update_user_by_id">
            update ebt_user
            <set>
                <if test="name is not None">name=${name}</if>
                <if test="age is not None">age=${age}</if>
                <if test="account is not None">account=${account}</if>
                <if test="address is not None">address=${address}</if>
            </set>
            where id=${id}
        </update>
        
        <insert id="insert_user">
            insert into ebt_user values(${name}, ${age}, ${account})
        </insert>
        
        <delete id="delete_user">
            delete from ebt_user where id=${id}
        </delete>
    </mapper>


## 4. 总结
这个也就是一个从xml到sql语句的映射工具，没什么厉害的功能，而且限制比较多，毕竟水平有限，也就是写来玩玩，练个手，不过我觉得拼接sql语句真的是一件痛苦而且无聊的事，
所以我真的很希望有一个还用的库，早日摆脱这个玩意...
