# 日志

### mysql错误日志
错误日志记录的事件：    
a)、服务器启动关闭过程中的信息   
b)、服务器运行过程中的错误信息       
c)、事件调试器运行一个事件时间生的信息        
d)、在从服务器上启动从服务器进程时产生的信息        
log_error参数指定错误日志存放路径以及文件名。如果不指定文件，默认文件名是[host_name].err，保存路径为%datadir%。     
错误日志中记录的信息分为三类：[Note]，[warning]，[Error]。可以通过设置log_warnings来控制警告信息是否被记录，默认值为1表示记录，为0表示禁用。如果大于1，则对于连接失败、新连接拒绝等类型的消息也会被写入到错误日志中去。     
   
### mysql的查询日志
查询日志记录查询语句与启动时间，建议不是在调试环境下不要开启查询日志，因为会不断占据你的磁盘空间，并会产生大量的IO。     
查询日志有两种，分别是慢查询日志（Slow Query Log）和通用查询日志（General Query Log）。而且mysql的查询日志不仅可以记录到文件，还能自动保存到MySql数据库中的表对象里。     

#### 1、慢查询日志    
指的是所有查询语句执行时间超过系统变量long_query_time（默认值是10秒）指定的参数值，并且访问的记录数超过系统变量min_examined_row_limit（默认值是0条）的数量的语句。这里的执行时间是不包括初始化表锁的开销。    
   
慢查询日志中语句记录和顺序有可能跟执行顺序不同，因为每条语句执行完并且释放了锁资源之后，mysqld才会将符合条件的sql语句写入到慢查询日志中去。         
开启和禁用慢查询日志通过以下两个系统参数，这两个参数可以动态修改：    
slow_query_log  指定是否输出慢查询日志，1表示输出，0表示不输出，默认为0。    
slow_query_log_file   指定日志文件存储路径和文件名，如果没有指定，默认文件名为[host_name]-slow.log，保存路径为%datadir%。      
全局禁用/开启慢查询日志:     
SET GLOBAL slow_query_log='OFF';     
SET GLOBAL slow_query_log='ON';    
其他参数：   
long_query_time   
log_short_format    
log_slow_admin_statements    
log_queries_not_using_indexes   
log_throttle_queries_not_using_indexes    
log_slow_slave_statements    
mysqld判断一条sql语句是否需要被记录到慢查询日志时做的判断步骤如下：
1）判断执行的是查询语句，还是管理性语句
2）查询语句执行的时间达到或者超过了long_query_time参数值，或者是符合log_queries_not_using_indexes条件
3）查询的记录量达到了min_examined_row_limit参数值
4）查询语句不违反log_throttle_queries_not_using_indexes设定的值
如果慢查询日志非常大，可以用mysql自带的mysqldumpslow命令，或者其他第三方工具查看分析。      

#### 2、通用查询日志
这个日志可以记录mysqld进程所做的几乎所有操作，包括sql语句执行，数据库对象管理，客户端的连接和断开。    
这个日志的最大功能是审计。    
开启和禁用通用查询日志通过以下两个系统参数，这两个参数可以动态修改：   
general_log   指定是否输出慢查询日志，1表示输出，0表示不输出，默认为0。    
general_log_file   指定日志文件存储路径和文件名，如果没有指定，默认文件名为[host_name].log，保存路径为%datadir%。    
全局禁用/开启通用日志:    
SET GLOBAL general_log='OFF';    
SET GLOBAL general_log='ON';    
会话级禁用/开启通用日志:   
SET sql_log_off='OFF';     
SET sql_log_off='ON';    
通用查询日志文件中语句出现的顺序，是按照mysqld接收的顺序。     

#### 3、配置查询日志：
在mysql服务启动时指定--log-output选项，可以决定查询日志是保存在操作系统中的文件里，还是保存在数据库系统中的专用表。    
--log-output  可选值有三个：table，输出到表，对应的表有general_log和slow_log     
                            file，输出到日志文件   
                            none，不输出查询日志     
--log-output可以设定多个值。    
默认情况下，日志表使用CSV引擎，5.1以后，日志表也可以修改为MyIsam引擎。      
日志表（general_log和slow_log）支持create table，alter table，drop table，truncate table，rename，check。不支持lock tables，insert，update，delete操作，日志表的增删改查均由mysql服务内部自己进行。                
flush tables with read lock以及设置全局系统变量read_only，对日志表无效。    
日志表的写操作不会计入二进制日志，有复制环境的话，日志表的内容也不会被复制到其他Slaves节点。    
用flush tables或flush logs来刷新日志表或者日志文件。    
日志表不允许创建分区。    



###  二进制日志文件：
通过二进制日志文件，可以主要实现三个重要的功能：用于复制，用于恢复，用于审计。     
启用二进制日志文件，在mysql服务启动时添加参数log-bin=[base_name]。如果不指定参数值，默认文件名为[host_name]-bin.log，保存路径为%datadir%。    

二进制日志文件不会只有一个，从序号1开始起，每次启动mysql服务或者刷新日志时，生成一个新的二进制日志文件。而且单个日志文件不可能无限增长，当涨到参数max_binlog_size指定的大小时，就会创建新的二进制日志文件。但是也有可能日志文件比max_binlog_size指定的值要大，假如有执行的事务很大，所有的事务信息必须写到一个日志文件中去。        
为了跟踪二进制日志文件的状态，mysql服务创建了一个和二进制日志文件同名，但是扩展名为.index的二进制日志索引文件。这个文件中包含所有可供使用的二进制日志文件。      
如果拥有super权限的用户执行操作前，执行了set sql_log_bin=0命令，则会禁止其执行的语句生产二进制日志。       
--binlog-do-db和--binlog-ignore-db两个选项，表示指定那些库记录或者不记录二进制日志，这两个选项每次只能设定一个值，如果有多个库，反复设置多条。     
二进制日志文件的格式有三种：基于行格式记录（row-based logging）、基于语句记录（statement-based logging）、混合模式记录（mixed-based logging）。      
因为mysql中既有支持事务的存储引擎，也有不支持事务的存储引擎，因此在操作基于不同的存储引擎对象时，二进制日志的处理也不一样。     
对于非事务表来说，语句执行后就会立即写入二进制日志文件中。而对于事务表，则要到等到当前没有任何锁定或未提交的信息时才会写入二进制日志文件中，以确保日志被记录的始终是其执行的顺序。     
 
###  事务日志：
事务日志文件名为"ib_logfile0"和“ib_logfile1”，默认存放在表空间所在目录     

与事务日志相关变量：      
``` sql
 #设定InnoDB重做日志文件的存储目录。在缺省使用InnoDB日志相关的所有变量时，其默认会在数据目录中创建两个大小为5MB的名为ib_logfile0和ib_logfile1的日志文件。作用范围为全局级别，可用于选项文件，属非动态变量。
innodb_log_group_home_dir=/PATH/TO/DIR  
#设定日志组中每个日志文件的大小，单位是字节，默认值是5MB。较为明智的取值范围是从1MB到缓存池体积的1/n，其中n表示日志组中日志文件的个数。日志文件越大，在缓存池中需要执行的检查点刷写操作就越少，这意味着所需的I/O操作也就越少，然而这也会导致较慢的故障恢复速度。作用范围为全局级别，可用于选项文件，属非动态变量。
innodb_log_file_size={108576 .. 4294967295}  
 #设定日志组中日志文件的个数。InnoDB以循环的方式使用这些日志文件。默认值为2。作用范围为全局级别，可用于选项文件，属非动态变量。
innodb_log_files_in_group={2 .. 100} 
# 设定InnoDB用于辅助完成日志文件写操作的日志缓冲区大小，单位是字节，默认为8MB。较大的事务可以借助于更大的日志缓冲区来避免在事务完成之前将日志缓冲区的数据写入日志文件，以减少I/O操作进而提升系统性能。因此，在有着较大事务的应用场景中，建议为此变量设定一个更大的值。作用范围为全局级别，可用于选项文件，属非动态变量。
innodb_log_buffer_size={262144 .. 4294967295}  
#表示有事务提交后，不会让事务先写进buffer，再同步到事务日志文件，而是一旦有事务提交就立刻写进事务日志，并且还每隔1秒钟也会把buffer里的数据同步到文件，这样IO消耗大，默认值是"1"，可修改为“2”
innodb_flush_log_at_trx_commit = 1  
#这个变量建议保持OFF状态，详细的原理不清楚
innodb_locks_unsafe_for_binlog = OFF 
 #事务日志组保存的镜像数
innodb_mirrored_log_groups = 1   
```

#### 中继日志：
在复制环境中产的的日志信息   
与中继日志相关的变量：    
``` sql
log_slave_updates   #用于设定复制场景中的从服务器是否将从主服务器收到的更新操作记录进本机的二进制日志中。本参数设定的生效需要在从服务器上启用二进制日志功能。
relay_log=file_name  #设定中继日志的文件名称，默认为host_name-relay-bin。也可以使用绝对路径，以指定非数据目录来存储中继日志。作用范围为全局级别，可用于选项文件，属非动态变量。
relay_log_index=file_name   #设定中继日志的索引文件名，默认为为数据目录中的host_name-relay-bin.index，作用范围为全局级别，可用于选项文件，属非动态变量。
relay-log-info-file=file_name  #设定中继服务用于记录中继信息的文件，默认为数据目录中的relay-log.info。作用范围为全局级别，可用于选项文件，属非动态变量。
relay_log_purge={ON|OFF}   #设定对不再需要的中继日志是否自动进行清理。默认值为ON。作用范围为全局级别，可用于选项文件，属动态变量。
relay_log_space_limit=      #设定用于存储所有中继日志文件的可用空间大小。默认为0，表示不限定。最大值取决于系统平台位数。作用范围为全局级别，可用于选项文件，属非动态变量。
max_relay_log_size={4096..1073741824}    #设定从服务器上中继日志的体积上限，到达此限度时其会自动进行中继日志滚动。此参数值为0时，mysqld将使用max_binlog_size参数同时为二进制日志和中继日志设定日志文件体积上限。作用范围为全局级别，可用于配置文件，属动态变量。
```

# 性能分析与explain
## 检查分析步骤

### 1.检查系统的状态
 通过操作系统的一些工具检查系统的状态，比如CPU、内存、交换、磁盘的利用率、IO、网络，根据经验或与系统正常时的状态相比对，有时系统表面上看起来看空闲，这也可能不是一个正常的状态，因为cpu可能正等待IO的完成。除此之外，还应观注那些占用系统资源(cpu、内存)的进程。（这一步不详细阐述）
 
### 2.检查mysql参数
 几个不被注意的mysql参数
1.1 max_connect_errors
 max_connect_errors默认值为10，如果受信帐号错误连接次数达到10则自动堵塞，需要flush hosts来解除。如果你得到象这样的一个错误：Host ’hostname’ is blocked because of many connection errors. Unblock with ’mysqladmin flush-hosts’这意味着，mysqld已经得到了大量(max_connect_errors)的主机’hostname’的在中途被中断了的连接请求。在 max_connect_errors次失败请求后，mysqld认定出错了(象来字一个黑客的攻击)，并且阻止该站点进一步的连接，直到某人执行命令 mysqladmin flush-hosts。内网连接的话，建议设置在10000以上，已避免堵塞，并定期flush hosts。    

1.2 connect_timeout         
 指定MySQL服务等待应答一个连接报文的最大秒数，超出该时间，MySQL向客户端返回 bad handshake。默认值是5秒，在内网高并发环境中建议设置到10-15秒，以便避免bad hand shake。建议同时关注thread_cache_size并设置thread_cache_size为非0值，大小具体调整。     

1.3 skip-name-resolve       
skip-name-resolve能大大加快用户获得连接的速度，特别是在网络情况较差的情况下。MySQL在收到连接请求的时候，会根据请求包中获得的ip来反向追查请求者的主机名。然后再根据返回的主机名又一次去获取ip。如果两次获得的ip相同，那么连接就成功建立了。在DNS不稳定或者局域网内主机过多的情况下，一次成功的连接将会耗费很多不必要的时间。假如MySQL服务器的ip地址是广域网的，最好不要设置skip-name- resolve。   

1.4 slave-net-timeout=seconds       
参数含义：当slave从主数据库读取log数据失败后，等待多久重新建立连接并获取数据。默认值是3600秒，如果需要保证同步性，如此NC的参数请极力控制在10秒以下
   
1.5 master-connect-retry      
参数含义：当重新建立主从连接时，如果连接建立失败，间隔多久后重试。默认是60秒，请按照合理的情况去设置参数。    

### 3.检查mysql 相关状态
 几个命令：
 show status           显示系统状态 
 show variables     显示系统变量
 show processlist   显示进程状态
 show profiles;       收集执行查询资源信息 默认是关闭的 开启 set profiling=1;

#### 1．连接数
mysql> show variables like 'max_connections';  最大连接数       
mysql> show status like 'max_used_connections';  响应的连接数       
一般情况下，max_used_connections的值在max_connections的85%左右是比较合适的     

#### 2．连接失败情况    
``` sql
mysql> show status like'%aborted%';
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| Aborted_clients  | 46    |
| Aborted_connects | 1     |
+------------------+-------+
```
2 rows in set (0.00 sec)
参数：    
*  aborted_connects：连接mysql失败次数，如果指过高，那就该检查一下网络，错误链接失败会在此记录。         
*  aborted_clients：客户端非法中断连接次数。如果随时间而增大，看看mysql的链接是否正常，或者检查一下网络，或者检查一下max_allowed_packet，超过此设置的查询会被中断（ show variables like'%max%'）。     

3．慢查询（slow query）日志    
日志必然会拖慢系统速度，特别是CPU资源，所以如果CPU资源充分，可以一直打开，如果不充足，那就在需要调整的时候，或者在replication从服务器上打开（针对select）。

``` sql
mysql> show variables like ‘%slow%’;

+———————+—————————————-+

| Variable_name       | Value                                  |

+———————+—————————————-+

| log_slow_queries    | OFF                                    |

| slow_launch_time    | 2                                      |

| slow_query_log      | OFF                                    |

| slow_query_log_file | /data/mysql/data/mysql1-slow.log |

+———————+—————————————-+
```
参数：

* log_slow_queries：是否记录慢日志，用long_query_time变量的值来确定“慢查询”。      

* slow_launch_time：如果创建线程的时间超过该秒数，服务器增加Slow_launch_threads状态变量    

* slow_query_log：是否打开日志记录    

* slow_query_log_file：日志文件     
mysql> set global slow_query_log='ON'   注：打开日志记录,一旦slow_query_log变量被设置为ON，mysql会立即开始记录    

#### 4.缓存簇分析
缓存使用情况分析
show status like 'key_blocks_u%';             -----使用和未使用缓存簇(blocks)数     
show variables like '%Key_cache%';      
show variables like '%Key_buffer_size%'; 

#### 5．键值缓存(索引块缓冲区)   
mysql> show variables like 'key_buffer_size';     

#### 6．查询缓存    
很多应用程序都严重依赖于数据库，但却会反复执行相同的查询。每次执行查询时，数据库都必须要执行相同的工作 —— 对查询进行分析，确定如何执行查询，从磁盘中加载信息，然后将结果返回给客户机。MySQL 有一个特性称为查询缓存，查询缓存会存储一个 SELECT 查询的文本与被传送到客户端的相应结果。如果之后接收到一个同样的查询，服务器将从查询缓存中检索结果，而不是再次分析和执行这个同样的查询。在很多情况下，这会极大地提高性能。不过，问题是查询缓存在默认情况下是禁用的。      
  如果你有一个不经常改变的表并且服务器收到该表的大量相同查询，查询缓存在这样的应用环境中十分有用。对于许多Web服务器来说存在这种典型情况，它根据数据库内容生成大量的动态页面。      
服务器启动时要禁用查询缓存，设置query_cache_size系统变量为0。禁用查询缓存代码后，没有明显的速度提高。编译MySQL时，通过在configure中使用--without-query-cache选项，可以从服务器中彻底去除查询缓存能力。      
mysql> show variables like 'have_query_cache';      

#### 7．线程使用情况        
mysql> show status like 'Thread%';      


#### 8．打开的文件数    
mysql> show status like '%open%file%';    

#### 9．打开表情况    
mysql> show status like 'open%tables%';     

#### 10．系统锁（表锁/行锁）情况     
mysql> show status like ‘%lock%’;     
 * Table_locks_immediate：     产生表级锁定的次数(立即获得的表的锁的次数)；            
* Table_locks_waited：           出现表级锁定争用而发生等待的次数(不能立即获得的表的锁的次数)。            

这两个状态变量记录MySQL内部表级锁定的情况，两个状态值都是从系统启动后开始记录，每出现一次对应的事件则数量加1。如果这里的Table_locks_waited状态值比较高，那么说明系统中表级锁定争用现象比较严重，就须要进一步分析为什么会为有较多的锁定资源争用了。由于Table_locks_waited显示了多少表被锁住并导致了mysql的锁等待，可以开启慢查询看一下。     

 对于InnoDB所使用的行级锁定，系统是通过另外一组更为详细的状态变量来记录的InnoDB的行级锁定状态变量不仅记录了锁定等待的次数，还记录了锁定总时长、每次平均时长、以及最大时长，此外还有一个非累计状态量显示了当前正在等待的数量。对各个状态的说明如下：     

* Innodb_row_lock_current_waits：当前正在等待锁定的数量         
* Innodb_row_lock_time ：             从系统启动到现在锁定的总时间长度(行锁定用的总时间(ms))    
* Innodb_row_lock_time_avg ：     每次等待所花平均时间(行锁定的平均时间(ms))，该值大，说明锁冲突大            
* Innodb_row_lock_time_max：     从系统启动到现在等待最长的一次所花的时间(行锁定的最长时间(ms))；          
* Innodb_row_lock_waits ：            从系统启动到现在总共等待的次数(行锁定必须等待的时间(ms))，该值大，说明锁冲突大         

#### 11．表扫描情况    
 mysql> show status like 'handler_read%';      
 
####  12．排序情况    
mysql> show variables like 'sort_buffer_size';    
* sort_buffer_size：每个排序线程分配的缓冲区的大小。增加该值可以加快ORDER BY或GROUP BY操作。
   
#### 13．全联接    
mysql> show  status like '%select_full__%';    

#### 14．临时表情况     
mysql>  show  status like 'created_tmp%';     

#### 15．二进制日志缓存     
mysql> show status like'%binlog%';     

#### 16．InnoDB相关状态     
关于InnoDB的性能分析，MySQL官方文档中有一节作专门分析：InnoDB性能调节揭示。    
show variables like 'innodb%';     

以上内容参考阅读：http://www.cnblogs.com/jevo/p/3314361.html


### explain用法
MySQL的EXPLAIN命令用于SQL语句的查询执行计划(QEP)。这条命令的输出结果能够让我们了解MySQL 优化器是如何执行SQL 语句的。这条命令并没有提供任何调整建议，但它能够提供重要的信息帮助你做出调优决策。      

#### 语法：
EXPLAIN tbl_name    
或：   
EXPLAIN [EXTENDED] SELECT select_options   
前者可以得出一个表的字段结构等等，后者主要是给出相关的一些索引信息，而今天要讲述的重点是后者。    

举例  
``` sql
mysql> explain select * from event;
+—-+————-+——-+——+—————+——+———+——+——+——-+
| id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra |
+—-+————-+——-+——+—————+——+———+——+——+——-+
| 1 | SIMPLE | event | ALL | NULL | NULL | NULL | NULL | 13 | |
+—-+————-+——-+——+—————+——+———+——+——+——-+
1 row in set (0.00 sec)
```
各个属性的含义   
#### id
select查询的序列号 

#### key    
 key 列指出优化器选择使用的索引。一般来说SQL 查询中的每个表都仅使用一个索引。也存在索引合并的少数例外情况，如给定表上用到了两个或者更多索引。如果没有索引被选择，键是NULL。        
 下面是QEP 中key 列的示例：    
 key: item_id   
 key: NULL   
 key: first, last    
 SHOW CREATE TABLE <table>命令是最简单的查看表和索引列细节的方式。和key 列相关的列还包括possible_keys、rows 以及key_len。
 
#### ROWS
这个数表示mysql要遍历多少数据才能找到，在innodb上是不准确的。rows 列提供了试图分析所有存在于累计结果集中的行数目的MySQL 优化器估计值。QEP 很容易描述这个很困难的统计量。查询中总的读操作数量是基于合并之前行的每一行的rows 值的连续积累而得出的。这是一种嵌套行算法。     
以连接两个表的QEP 为例。通过id=1 这个条件找到的第一行的rows 值为1，这等于对第一个表做了一次读操作。第二行是通过id=2 找到的，rows 的值为5。这等于有5 次读操作符合当前1 的积累量。参考两个表，读操作的总数目是6。在另一个QEP中，第一rows 的值是5，第二rows 的值是1。这等于第一个表有5 次读操作，对5个积累量中每个都有一个读操作。因此两个表总的读操作的次数是10(5+5)次。     
最好的估计值是1，一般来说这种情况发生在当寻找的行在表中可以通过主键或者唯一键找到的时候。
 
#### possible_keys
指出MySQL能使用哪个索引在该表中找到行。如果是空的，没有相关的索引。这时要提高性能，可通过检验WHERE子句，看是否引用某些字段，或者检查字段不是适合索引。 一个会列出大量可能的索引(例如多于3 个)的QEP 意味着备选索引数量太多了，同时也可能提示存在一个无效的单列索引。

 
#### key_len
显示MySQL决定使用的键长度。如果键是NULL，长度就是NULL。文档提示特别注意这个值可以得出一个多重主键里mysql实际使用了哪一部分。此列值对于确认索引的有效性以及多列索引中用到的列的数目很重要。
 此列的一些示例值如下所示：       
 key_len: 4 // INT NOT NULL   
 key_len: 5 // INT NULL     
 key_len: 30 // CHAR(30) NOT NULL   
 key_len: 32 // VARCHAR(30) NOT NULL   
 key_len: 92 // VARCHAR(30) NULL CHARSET=utf8   
 
从这些示例中可以看出，是否可以为空、可变长度的列以及key_len 列的值只和用在连接和WHERE 条件中的索引的 有关。索引中的其他列会在ORDER BY 或者GROUP BY 语句中被用到。 

#### table
输出的行所引用的表。 是EXPLAIN 命令输出结果中的一个单独行的唯一标识符。这个值可能是表名、表的别名或者一个为查询产生临时表的标识符，如派生表、子查询或集合。   
 
#### select_type
select查询的类型，主要是区别普通查询和联合查询、子查询之类的复杂查询select_type 列提供了各种表示table 列引用的使用方式的类型。最常见的值包括SIMPLE、PRIMARY、DERIVED 和UNION。其他可能的值还有UNION RESULT、DEPENDENT SUBQUERY、DEPENDENT UNION、UNCACHEABLE UNION 以及UNCACHEABLE QUERY。
 1. SIMPLE    
 对于不包含子查询和其他复杂语法的简单查询，这是一个常 见的类型。    

 2. PRIMARY     
 这是为更复杂的查询而创建的首要表(也就是最外层的表)。这个类型通常可以在DERIVED 和UNION 类型混合使用时见到。      
 
 3. DERIVED     
 当一个表不是一个物理表时，那么就被叫做DERIVED。下面的SQL 语句给出了一个QEP 中DERIVED select-type 类型的      
 示例：
 mysql> EXPLAIN SELECT MAX(id)
 -> FROM (SELECT id FROM users WHERE first = 'west') c;

 4. DEPENDENT SUBQUERY    
 这个select-type 值是为使用子查询而定义的。 

 5. UNION     
 这是UNION 语句其中的一个SQL 元素。    
 
 6. UNION RESULT      
 这是一系列定义在UNION 语句中的表的返回结果。当select_type 为这个值时，经常可以看到table 的值是<unionN,M>，
     
#### type
联合查询所使用的类型。type显示的是访问类型，是较为重要的一个指标，结果值从好到坏依次是：
system > const > eq_ref > ref > fulltext > ref_or_null > index_merge > unique_subquery > index_subquery > range > index > ALL       
一般来说，得保证查询至少达到range级别，最好能达到ref。    

#### ref
ref 列可以被用来标识那些用来进行索引比较的列或者常量。

#### Extra
Extra 列提供了有关不同种类的MySQL 优化器路径的一系列额外信息。Extra 列可以包含多个值，可以有很多不同的取值，并且这些值还在随着MySQL 新版本的发布而进一步增加。下面给出常用值的列表。     
如果是Only index，这意味着信息只用索引树中的信息检索出的，这比扫描整个表要快。     
如果是where used，就是使用上了where限制。     
如果是impossible where 表示用不着where，一般就是没查出来啥。     
如果此信息显示Using filesort或者Using temporary的话会很吃力，WHERE和ORDER BY的索引经常无法兼顾，如果按照WHERE来确定索引，那么在ORDER BY时，就必然会引起Using filesort，这就要看是先过滤再排序划算，还是先排序再过滤划算。      

1. Using where
这个值表示查询使用了where 语句来处理结果——例如执行全表扫描。如果也用到了索引，那么行的限制条件是通过获取必要的数据之后处理读缓冲区来实现的。

2. Using temporary
这个值表示使用了内部临时(基于内存的)表。一个查询可能用到多个临时表。有很多原因都会导致MySQL 在执行查询期间创建临时表。两个常见的原因是在来自不同表的列上使用了DISTINCT，或者使用了不同的ORDER BY 和GROUP BY 列。of_query_execution_and_use_of_temp_tables。可以强制指定一个临时表使用基于磁盘MyISAM 存储引擎。这样做的原因主要有两个：
内部临时表占用的空间超过min(tmp_table_size，max_ heap_table_size)系统变量的限制,使用了TEXT/BLOB 列

3. Using filesort       
这是ORDER BY 语句的结果。这可能是一个CPU 密集型的过程。可以通过选择合适的索引来改进性能，用索引来为查询结果排序。    

4. Using index    
这个值重点强调了只需要使用索引就可以满足查询表的要求，不需要直接访问表数据。请参考第5 章的详细示例来理解这个值。     

5. Using join buffer      
这个值强调了在获取连接条件时没有使用索引，并且需要连接缓冲区来存储中间结果。 如果出现了这个值，那应该注意，根据查询的具体情况可能需要添加索引来改进性能。       

6. Impossible where    
这个值强调了where 语句会导致没有符合条件的行。请看下面的示例：     
mysql> EXPLAIN SELECT * FROM user WHERE 1=2;    

7. Select tables optimized away      
这个值意味着仅通过使用索引，优化器可能仅从聚合函数结果中返回一行。请看下面的示例：     

8. Distinct    
这个值意味着MySQL在找到第一个匹配的行之后就会停止搜索其他行。     

9. Index merges     
当MySQL 决定要在一个给定的表上使用超过一个索引的时候，就会出现以下格式中的一个，详细说明使用的索引以及合并的类型。     
 Using sort_union(...)          
 Using union(...)     
 Using intersect(...)            

