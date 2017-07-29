

### 三大范式
第一范式:确保每列的原子性.     
第二范式:在第一范式的基础上更进一层,目标是确保表中的每列都和主键相关.     
第三范式:在第二范式的基础上更进一层,目标是确保每列都和主键列直接相关,而不是间接相关.      

### 基础操作
增       
INSERT INTO table_name VALUES (value1,value2,value3,...);    
或    
INSERT INTO table_name (column1,column2,column3,...) VALUES (value1,value2,value3,...);      

删   
DELETE FROM table_name WHERE some_column=some_value;    

改       
UPDATE table_name SET column1=value1,column2=value2,...WHERE some_column=some_value;       

查   
SELECT column_name,column_name FROM table_name;   


#### 操作符
用来联结或改变WHERE子句中的子句的关键字。

AND    
用来指示检索满足 所有 给定条件的行。   
OR      
用来表示检索匹配 任一 给定条件的行。   
IN       
用在WHERE子句中的关键字，用来指定要匹配值的清单的关键字(取合法值的由逗号分割开的清单，全在圆括号中)，功能与OR相当。    
NOT   
用在WHERE子句中的关键字，用来否定它之后所跟的任何条件。   
BETWEEN     
用在WHERE子句中的关键字，用来检查某个范围的值。     
通配符         
用来匹配值的一部分的特殊字符。为在搜索子句中使用通配符，必须使用LIKE谓词。LIKE指示MySQL后跟的搜索模式利用通配符匹配而不是直接相等匹配进行比较。

%通配符：       
表示任何字符出现的任一次数。   
_通配符：     
下划线通配符 _ 用途与%一样，但下划线只匹配单个字符而不是多个字符。     

通配符使用技巧     
1、不要过度使用通配符。如果其他操作能达到相同的目的，应该使用其他操作符。         
2、在确实需要使用通配符时除非绝对有必要，否则不要把它们用在搜索模式的最开始处，因为这样是最慢的。      
3、仔细注意通配符的位置。如果放错地方，可能不会返回想要的数据。       


#### 计算字段
1、Concat拼接字段：
把多个串链接起来形成一个较长的串，需要一个或多个指定的串，各个串之间用逗号隔开。   
例如：SELECT Concat(vend_name,'(',vend_country,')') FROM vendors ORDER BY vend_name;
2、去掉返回的值中的空格：  
(1)、RTrim()去掉右侧多余的空格来整理数据。  
(2)、LTrim()去掉左侧多余的空格来整理数据。  
(3)、Trim()去掉左右两边多余的空格来整理数据。   
3、执行算数运算(MySQL支持 加减乘除运算和圆括号改变运算优先级)：  
计算字段另一个用途就是对检索出的数据进行算术计算。      
例如：SELECT prod_id, quantity, item_price, quantity * item_price AS expanded_price FROM orderitems WHERE order_num = 20005;

#### 事件处理函数
函数一般是在数据上执行的，它给数据的转换和处理提供了方便。大多数SQL实现支持用于处理文本串的函数、用于在数值数据上进行算术运算操作的函数、用于处理日期和时间并提取特定成分的日期和时间函数、返回DBMS正使用的特殊信息的函数
1、常见的文本处理函数：
(1)、Upper(str)：将文本str转换为大写。    
例：SELECT Upper(vend_name) AS vend_name_upcase FROM vendors ORDER BY vend_name;
(2)、Left(str, len)：返回串str左边的len个字符。      
例：SELECT Left(vend_name, 3) AS vend_name_upcase FROM vendors ORDER BY vend_name;
(3)、Length(str)：返回串str的长度。     
例：SELECT Length(vend_name) AS vend_name_upcase FROM vendors ORDER BY vend_name;
(4)、Locate(substr, str)：返回串str的一个substr子串的第一个字符出现的位置,如果substr不再str中则返回0。该函数的另一个版本是   Locate(substr,str,pos),表示从pos位置开始在str中寻找substr。
例：SELECT Locate('ACM', vend_name) FROM vendors ORDER BY vend_name;  

注意：
1、ORDER BY子句必须位于FROM子句之后。   
2、当ORDER BY 子句和LIMIT子句同时使用时LIMIT子句必须位于ORDER BY子句之后     
3、同时使用WHERE子句和ORDER BY子句时应将ORDER BY子句置于WHERE子句之后。      
4、WHERE子句支持 =、>、<、!=、<>(不等于)、>=、<=、BETWEEN(指定的两个值之间)过滤操作。   
5、AND和OR操作符混合使用时要注意AND操作符的计算次序比OR操作符号的计算次序要高(操作符优先级高)，所以一般有多个操作符时要加上圆括号消除歧义(即使不这样做也是正确的)       
6、MySQL支持使用NOT对IN、BETWEEN和EXISTS子句取反(其他DBMS允许使用NOT对各种条件取反)。
7、尾空格可能会干扰通配符匹配，例如：'%anvil'如果anvil后有一个空格则不会被匹配出来。可使用'%anvil%'或者使用函数解决此问题。
8、%通配符不会匹配到NULL。
9、SELECT语句的拼接完成的列是没有名字的，它只是一个值，这种是无法在客户机中直接使用的，所以可以用AS关键字赋予一个别名(也称为导出列)。
例如：SELECT Concat(vend_name,'(',vend_country,')') AS vend_title FROM vendors ORDER BY vend_name;

### 聚集函数：

运行在行组上，计算和返回单个值的函数（需要汇总数据而不需要检索出来）

ACG(column)：返回某列的平均值。  
COUNT(column)：返回某列的行数。  
COUNT(*)：返回所有列的和。  
MIN(column)：返回某列的最小值。  
MAX(column)：返回某列的最大值。  
SUM(column)：返回某列的和。  
DISTINCT：只包含不同值  
分组：
分组允许把数据分为多个逻辑组，以便能对每个组进行聚集计算。  

创建分组：GROUP BY子句，GROUP BY子句必须出现在WHERE子句之后，ORDER BY子句之前。   
WITH ROLLUP：可以得到每个分组汇总级别的值（和ORDER BY子句互斥）。   
HAVING：HAVING过滤分组，WHERE过滤列，HAVING位于GROUP BY子句之前，HAVING位于GROUP BY子句之后。（WHERE在分组前进行过滤，HAVING在分组后进行过滤）

GROUP BY和ORDER BY子句的区别：
1、OEDER BY是排序后的输出而GROUP BY是分组的顺序（不一定是期望输出的顺序）    
2、ORDER BY任意列都可以使用，而GROUP BY只可能使用选择列或表达式列，而且必须使用每个选择列表达式。  
3、ORDER BY不是必须出现在SQL语句中，但是如果与聚集函数一起使用列（或表达式）GROUP BY子句必须存在于SQL语句中。   


### 子查询  
1）子查询概念：当一个查询是另一个查询的子部分时，称之为子查询（查询语句中嵌套有查询语句）。   

子查询出现的位置有：

a）目标列位置：子查询如果位于目标列，则只能是标量子查询，否则数据库可能返回类似“错误:  子查询必须只能返回一个字段”的提示。

b）FROM子句位置：相关子查询出现在FROM子句中，数据库可能返回类似“在FROM子句中的子查询无法参考相同查询级别中的关系”的提示，所以相关子查询不能出现在FROM子句中；非相关子查询出现在FROM子句中，可上拉子查询到父层，在多表连接时统一考虑连接代价然后择优。

c）WHERE子句位置：出现在WHERE子句中的子查询，是一个条件表达式的一部分，而表达式可以分解为操作符和操作数；根据参与运算的不同的数据类型，操作符也不尽相同，如INT型有“>、<、=、<>”等操作，这对子查询均有一定的要求（如INT型的等值操作，要求子查询必须是标量子查询）。另外，子查询出现在WHERE子句中的格式，也有用谓词指定的一些操作，如IN、BETWEEN、EXISTS等。   

d）JOIN/ON子句位置：JOIN/ON子句可以拆分为两部分，一是JOIN块类似于FROM子句，二是ON子句块类似于WHERE子句，这两部分都可以出现子查询。子查询的处理方式同FROM子句和WHERE子句。      

e）GROUPBY子句位置：目标列必须和GROUPBY关联1。可将子查询写在GROUPBY位置处，但子查询用在GROUPBY处没有实用意义。

f）ORDERBY子句位置：可将子查询写在ORDERBY位置处。但ORDERBY操作是作用在整条SQL语句上的，子查询用在ORDERBY处没有实用意义。

### 子查询的优化方法

a）子查询合并（Subquery Coalescing）

在某些条件下（语义等价：两个查询块产生同样的结果集），多个子查询能够合并成一个子查询（合并后还是子查询，以后可以通过其他技术消除掉子查询）。这样可以把多次表扫描、多次连接减少为单次表扫描和单次连接，如：

SELECT * FROM t1 WHERE a1<10 AND (

EXISTS (SELECT a2 FROM t2 WHERE t2.a2<5 AND t2.b2=1) OR 

EXISTS (SELECT a2 FROM t2 WHERE t2.a2<5 AND t2.b2=2) 

);

可优化为：

SELECT * FROM t1 WHERE a1<10 AND (

EXISTS (SELECT a2 FROM t2 WHERE t2.a2<5 AND(t2.b2=1 OR t2.b2=2) 

/*两个ESISTS子句合并为一个，条件也进行了合并 */

);

b）子查询展开（Subquery Unnesting）

又称子查询反嵌套，又称为子查询上拉。把一些子查询置于外层的父查询中，作为连接关系与外层父查询并列，其实质是把某些子查询重写为等价的多表连接操作（展开后，子查询不存在了，外部查询变成了多表连接）。带来的好处是，有关的访问路径、连接方法和连接顺序可能被有效使用，使得查询语句的层次尽可能的减少。

常见的IN/ANY/SOME/ALL/EXISTS依据情况转换为半连接（SEMI JOIN）、普通类型的子查询消除等情况属于此类，如：

SELECT * FROM t1, (SELECT * FROM t2 WHERE t2.a2 >10)v_t2 

WHERE t1.a1<10 AND v_t2.a2<20;

可优化为：

SELECT * FROM t1, t2 WHERE t1.a1<10 AND t2.a2<20AND t2.a2 >10; 

/* 子查询变为了t1、t2表的连接操作，相当于把t2表从子查询中上拉了一层 */

子查询展开的条件：

a）如果子查询中出现了聚集、GROUPBY、DISTINCT子句，则子查询只能单独求解，不可以上拉到外层。

b）如果子查询只是一个简单格式的（SPJ格式）查询语句，则可以上拉子查询到外层，这样往往能提高查询效率。子查询上拉，讨论的就是这种格式，这也是子查询展开技术处理的范围。

把子查询上拉到上层查询，前提是上拉（展开）后的结果不能带来多余的元组，所以子查询展开需要遵循如下规则：

a）如果上层查询的结果没有重复（即SELECT子句中包含主码），则可以展开其子查询。并且展开后的查询的SELECT子句前应加上DISTINCT标志。

b）如果上层查询的SELECT语句中有DISTINCT标志，可以直接进行子查询展开。

如果内层查询结果没有重复元组，则可以展开。

子查询展开的具体步骤：

a）将子查询和外层查询的FROM子句连接为同一个FROM子句，并且修改相应的运行参数。

b）将子查询的谓词符号进行相应修改(如：“IN”修改为“=”)。

c）将子查询的WHERE条件作为一个整体与外层查询的WHERE条件合并，并用AND条件连接词连接，从而保证新生成的谓词与原旧谓词的上下文意思相同，且成为一个整体。

c）聚集子查询消除（Aggregate Subquery Elimination）

通常，一些系统支持的是标量聚集子查询消除。如：

SELECT * FROM t1 WHERE t1.a1>(SELECT avg(t2.a2) FROM t2);



关键字
DISTINCT 


### join
INNER JOIN：如果表中有至少一个匹配，则返回行
LEFT JOIN：即使右表中没有匹配，也从左表返回所有的行
RIGHT JOIN：即使左表中没有匹配，也从右表返回所有的行
FULL JOIN：只要其中一个表中存在匹配，则返回行

join优化

