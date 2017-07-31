# 日志

### mysql错误日志：
错误日志记录的事件：    
a)、服务器启动关闭过程中的信息   
b)、服务器运行过程中的错误信息    
c)、事件调试器运行一个事件时间生的信息    
d)、在从服务器上启动从服务器进程时产生的信息    
log_error参数指定错误日志存放路径以及文件名。如果不指定文件，默认文件名是[host_name].err，保存路径为%datadir%。     
错误日志中记录的信息分为三类：[Note]，[warning]，[Error]。可以通过设置log_warnings来控制警告信息是否被记录，默认值为1表示记录，为0表示禁用。如果大于1，则对于连接失败、新连接拒绝等类型的消息也会被写入到错误日志中去。
   
### mysql的查询日志：
查询日志记录查询语句与启动时间，建议不是在调试环境下不要开启查询日志，因为会不断占据你的磁盘空间，并会产生大量的IO。   
查询日志有两种，分别是慢查询日志（Slow Query Log）和通用查询日志（General Query Log）。而且mysql的查询日志不仅可以记录到文件，还能自动保存到MySql数据库中的表对象里。
1、慢查询日志：    
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

2、通用查询日志：
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
3、配置查询日志：
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



三、  二进制日志文件：
通过二进制日志文件，可以主要实现三个重要的功能：用于复制，用于恢复，用于审计。
启用二进制日志文件，在mysql服务启动时添加参数log-bin=[base_name]。如果不指定参数值，默认文件名为[host_name]-bin.log，保存路径为%datadir%。

二进制日志文件不会只有一个，从序号1开始起，每次启动mysql服务或者刷新日志时，生成一个新的二进制日志文件。而且单个日志文件不可能无限增长，当涨到参数max_binlog_size指定的大小时，就会创建新的二进制日志文件。但是也有可能日志文件比max_binlog_size指定的值要大，假如有执行的事务很大，所有的事务信息必须写到一个日志文件中去。
为了跟踪二进制日志文件的状态，mysql服务创建了一个和二进制日志文件同名，但是扩展名为.index的二进制日志索引文件。这个文件中包含所有可供使用的二进制日志文件。
如果拥有super权限的用户执行操作前，执行了set sql_log_bin=0命令，则会禁止其执行的语句生产二进制日志。
--binlog-do-db和--binlog-ignore-db两个选项，表示指定那些库记录或者不记录二进制日志，这两个选项每次只能设定一个值，如果有多个库，反复设置多条。
二进制日志文件的格式有三种：基于行格式记录（row-based logging）、基于语句记录（statement-based logging）、混合模式记录（mixed-based logging）。
因为mysql中既有支持事务的存储引擎，也有不支持事务的存储引擎，因此在操作基于不同的存储引擎对象时，二进制日志的处理也不一样。
对于非事务表来说，语句执行后就会立即写入二进制日志文件中。而对于事务表，则要到等到当前没有任何锁定或未提交的信息时才会写入二进制日志文件中，以确保日志被记录的始终是其执行的顺序。
 
四、  事务日志：
事务日志文件名为"ib_logfile0"和“ib_logfile1”，默认存放在表空间所在目录
与事务日志相关变量：
innodb_log_group_home_dir=/PATH/TO/DIR    #设定InnoDB重做日志文件的存储目录。在缺省使用InnoDB日志相关的所有变量时，其默认会在数据目录中创建两个大小为5MB的名为ib_logfile0和ib_logfile1的日志文件。作用范围为全局级别，可用于选项文件，属非动态变量。
innodb_log_file_size={108576 .. 4294967295}   #设定日志组中每个日志文件的大小，单位是字节，默认值是5MB。较为明智的取值范围是从1MB到缓存池体积的1/n，其中n表示日志组中日志文件的个数。日志文件越大，在缓存池中需要执行的检查点刷写操作就越少，这意味着所需的I/O操作也就越少，然而这也会导致较慢的故障恢复速度。作用范围为全局级别，可用于选项文件，属非动态变量。
innodb_log_files_in_group={2 .. 100}   #设定日志组中日志文件的个数。InnoDB以循环的方式使用这些日志文件。默认值为2。作用范围为全局级别，可用于选项文件，属非动态变量。
innodb_log_buffer_size={262144 .. 4294967295}   设定InnoDB用于辅助完成日志文件写操作的日志缓冲区大小，单位是字节，默认为8MB。较大的事务可以借助于更大的日志缓冲区来避免在事务完成之前将日志缓冲区的数据写入日志文件，以减少I/O操作进而提升系统性能。因此，在有着较大事务的应用场景中，建议为此变量设定一个更大的值。作用范围为全局级别，可用于选项文件，属非动态变量。
innodb_flush_log_at_trx_commit = 1  #表示有事务提交后，不会让事务先写进buffer，再同步到事务日志文件，而是一旦有事务提交就立刻写进事务日志，并且还每隔1秒钟也会把buffer里的数据同步到文件，这样IO消耗大，默认值是"1"，可修改为“2”
innodb_locks_unsafe_for_binlog = OFF   #这个变量建议保持OFF状态，详细的原理不清楚
innodb_mirrored_log_groups = 1    #事务日志组保存的镜像数
 
五、  中继日志：
在复制环境中产的的日志信息
与中继日志相关的变量：
log_slave_updates   #用于设定复制场景中的从服务器是否将从主服务器收到的更新操作记录进本机的二进制日志中。本参数设定的生效需要在从服务器上启用二进制日志功能。
relay_log=file_name  #设定中继日志的文件名称，默认为host_name-relay-bin。也可以使用绝对路径，以指定非数据目录来存储中继日志。作用范围为全局级别，可用于选项文件，属非动态变量。
relay_log_index=file_name   #设定中继日志的索引文件名，默认为为数据目录中的host_name-relay-bin.index，作用范围为全局级别，可用于选项文件，属非动态变量。
relay-log-info-file=file_name  #设定中继服务用于记录中继信息的文件，默认为数据目录中的relay-log.info。作用范围为全局级别，可用于选项文件，属非动态变量。
relay_log_purge={ON|OFF}   #设定对不再需要的中继日志是否自动进行清理。默认值为ON。作用范围为全局级别，可用于选项文件，属动态变量。
relay_log_space_limit=      #设定用于存储所有中继日志文件的可用空间大小。默认为0，表示不限定。最大值取决于系统平台位数。作用范围为全局级别，可用于选项文件，属非动态变量。
max_relay_log_size={4096..1073741824}    #设定从服务器上中继日志的体积上限，到达此限度时其会自动进行中继日志滚动。此参数值为0时，mysqld将使用max_binlog_size参数同时为二进制日志和中继日志设定日志文件体积上限。作用范围为全局级别，可用于配置文件，属动态变量。
 

