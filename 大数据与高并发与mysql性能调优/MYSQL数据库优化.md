## 单机MySQL数据库的优化
### 服务器硬件对MySQL性能的影响
　　①磁盘寻道能力 （磁盘I/O），我们现在上的都是SAS15000转的硬盘。MySQL每秒钟都在进行大量、复杂的查询操作，对磁盘的读写量可想而知。所以，通常认为磁 盘I/O是制约MySQL性能的最大因素之一，对于日均访 问量在100万PV以上的Discuz!论坛，由于磁盘I/O的制约，MySQL的性能会非常低下！解决这一制约因素可以考虑以下几种解决方案： 使用RAID1+0磁盘阵列，注意不要尝试使用RAID-5，MySQL在RAID-5磁盘阵列上的效率不会像你期待的那样快。      
　　②CPU 对于MySQL应用，推荐使用DELL R710，E5620 @2.40GHz（4 core）* 2 ，我现在比较喜欢DELL R710，也在用其作Linuxakg 虚拟化应用；        
　　③物理内存对于一台使用MySQL的Database Server来说，服务器内存建议不要小于2GB，推荐使用4GB以上的物理内存，不过内存对于现在的服务器而言可以说是一个可以忽略的问题，工作中遇到高端服务器基本上内存都超过了32G。       
　　我们工作中用得比较多的数据库服务器是HP DL580G5和DELL R710，稳定性和性能都不错；特别是DELL R710，我发现许多同行都是采用它作数据库的服务器，所以重点推荐下。     
### 二、MySQL的线上安装我建议采取编译安装的方法
这样性能上有较大提升，服务器系统我建议用64bit的Centos5.5，源码包的编译参数会默 认以Debgu模式生成二进制代码，而Debug模式给MySQL带来的性能损失是比较大的，所以当我们编译准备安装的产品代码时，一定不要忘记使用“— without-debug”参数禁用Debug模式。而如果把—with-mysqld-ldflags和—with-client-ldflags二 个编译参数设置为—all-static的话，可以告诉编译器以静态方式编译和编译结果代码得到最高的性能。使用静态编译和使用动态编译的代码相比，性能 差距可能会达到5%至10%之多。

### 三、MySQL自身因素
当解决了上述服务器硬件制约因素后，让我们看看MySQL自身的优化是如何操作的。对 MySQL自身的优化主要是对其配置文件my.cnf中的各项参数进行优化调整。下面我们介绍一些对性能影响较大的参数。     
下面，我们根据以上硬件配置结合一份已经优化好的my.cnf进行说明：
  

　　#vim /etc/my.cnf
　　以下只列出my.cnf文件中[mysqld]段落中的内容，其他段落内容对MySQL运行性能影响甚微，因而姑且忽略。
　　[mysqld]
　　port = 3306
　　serverid = 1
　　socket = /tmp/mysql.sock
　　skip-locking
　　#避免MySQL的外部锁定，减少出错几率增强稳定性。
　　skip-name-resolve
　　#禁止MySQL对外部连接进行DNS解析，使用这一选项可以消除MySQL进行DNS解析的时间。但需要注意，如果开启该选项，则所有远程主机连接授权都要使用IP地址方式，否则MySQL将无法正常处理连接请求！
　　back_log = 384
　 　#back_log参数的值指出在MySQL暂时停止响应新请求之前的短时间内多少个请求可以被存在堆栈中。 如果系统在一个短时间内有很多连接，则需要增大该参数的值，该参数值指定到来的TCP/IP连接的侦听队列的大小。不同的操作系统在这个队列大小上有它自 己的限制。 试图设定back_log高于你的操作系统的限制将是无效的。默认值为50。对于Linux系统推荐设置为小于512的整数。
　　key_buffer_size = 384M
　　#key_buffer_size指定用于索引的缓冲区大小，增加它可得到更好的索引处理性能。对于内存在4GB左右的服务器该参数可设置为256M或384M。注意：该参数值设置的过大反而会是服务器整体效率降低！
　　max_allowed_packet = 4M
　　thread_stack = 256K
　　table_cache = 614K
　　sort_buffer_size = 6M
　　#查询排序时所能使用的缓冲区大小。注意：该参数对应的分配内存是每连接独占，如果有100个连接，那么实际分配的总共排序缓冲区大小为100 × 6 ＝ 600MB。所以，对于内存在4GB左右的服务器推荐设置为6-8M。
　　read_buffer_size = 4M
　　#读查询操作所能使用的缓冲区大小。和sort_buffer_size一样，该参数对应的分配内存也是每连接独享。
　　join_buffer_size = 8M
　　#联合查询操作所能使用的缓冲区大小，和sort_buffer_size一样，该参数对应的分配内存也是每连接独享。
　　myisam_sort_buffer_size = 64M
　　table_cache = 512
　　thread_cache_size = 64
　　query_cache_size = 64M
　 　#指定MySQL查询缓冲区的大小。可以通过在MySQL控制台观察，如果Qcache_lowmem_prunes的值非常大，则表明经常出现缓冲不 够 的情况；如果Qcache_hits的值非常大，则表明查询缓冲使用非常频繁，如果该值较小反而会影响效率，那么可以考虑不用查询缓 冲；Qcache_free_blocks，如果该值非常大，则表明缓冲区中碎片很多。
　　tmp_table_size = 256M
　　max_connections = 768
　　#指定MySQL允许的最大连接进程数。如果在访问论坛时经常出现Too Many Connections的错误提 示，则需要增大该参数值。
　　max_connect_errors = 1000
　　wait_timeout = 10
　　#指定一个请求的最大连接时间，对于4GB左右内存的服务器可以设置为5-10。
　　thread_concurrency = 8
　　#该参数取值为服务器逻辑CPU数量*2，在本例中，服务器有2颗物理CPU，而每颗物理CPU又支持H.T超线程，所以实际取值为4*2=8；这个目前也是双四核主流服务器配置。
　　skip-networking
　　#开启该选项可以彻底关闭MySQL的TCP/IP连接方式，如果WEB服务器是以远程连接的方式访问MySQL数据库服务器则不要开启该选项！否则将无法正常连接！
　　table_cache=1024
　　#物理内存越大，设置就越大。默认为2402,调到512-1024最佳
　　innodb_additional_mem_pool_size=4M
　　#默认为2M
　　innodb_flush_log_at_trx_commit=1
　　#设置为0就是等到innodb_log_buffer_size列队满后再统一储存，默认为1
　　innodb_log_buffer_size=2M
　　#默认为1M
　　innodb_thread_concurrency=8
　　#你的服务器CPU有几个就设置为几，建议用默认一般为8
　　key_buffer_size=256M
　　#默认为218，调到128最佳
　　tmp_table_size=64M
　　#默认为16M，调到64-256最挂
　　read_buffer_size=4M
　　#默认为64K
　　read_rnd_buffer_size=16M
　　#默认为256K
　　sort_buffer_size=32M
　　#默认为256K
　　thread_cache_size=120
　　#默认为60
　　query_cache_size=32M

  
  
### 注意：
一、如果Key_reads太大，则应该把my.cnf中Key_buffer_size变大，保持Key_reads/Key_read_requests至少1/100以上，越小越好。
二、如果Qcache_lowmem_prunes很大，就要增加Query_cache_size的值。
很多时候我们发现，通过参数设置进行性能优化所带来的性能提升，可能并不如许多人想象的那样产生质的飞跃，除非是之前的设置存在严重不合理的情况。我们 不能将性能调优完全依托于通过DBA在数据库上线后进行的参数调整，而应该在系统设计和开发阶段就尽可能减少性能问题。

### MySQL的高可用架构
如果单MySQL的优化始终还是顶不住压力时，这个时候我们就必须考虑MySQL的高可用架构（很多同学也爱说成是MySQL集群）了，目前可行的方案有：
#### 一、MySQL Cluster
优势：可用性非常高，性能非常好。每份数据至少可在不同主机存一份拷贝，且冗余数据拷贝实时同步。但它的维护非常复杂，存在部分Bug，目前还不适合比较核心的线上系统，所以这个我不推荐。  
#### 二、DRBD磁盘网络镜像方案
优势：软件功能强大，数据可在底层快设备级别跨物理主机镜像，且可根据性能和可靠性要求配置不同级别的同步。IO操作保持顺序，可满足数据库对数据一致 性的苛刻要求。但非分布式文件系统环境无法支持镜像数据同时可见，性能和可靠性两者相互矛盾，无法适用于性能和可靠性要求都比较苛刻的环境，维护成本高于 MySQL Replication。另外，DRBD也是官方推荐的可用于MySQL高可用方案之一，所以这个大家可根据实际环境来考虑是否部署。
#### 三、MySQL Replication
在实际应用场景中，MySQL Replication是使用最为广泛的一种提高系统扩展性的设计手段。众多的MySQL使用者通过Replication功能提升系统的扩展性后，通过 简单的增加价格低廉的硬件设备成倍 甚至成数量级地提高了原有系统的性能，是广大MySQL中低端使用者非常喜欢的功能之一，也是许多MySQL使用者选择MySQL最为重要的原因。

比较常规的MySQL Replication架构也有好几种，这里分别简单说明下   
1.常规复制架构--Master-slaves，是由一个Master复制到一个或多个Salve的架构模式，主要用于读压力大的应用数据库端廉价扩展解决方案，读写分离，Master主要负责写方面的压力。   
2.级联复制架构，即Master-Slaves-Slaves,这个也是为了防止Slaves的读压力过大，而配置一层二级 Slaves，很容易解决Master端因为附属slave太多而成为瓶劲的风险。   
3.Dual Master与级联复制结合架构，即Master-Master-Slaves，最大的好处是既可以避免主Master的写操作受到Slave集群的复制带来的影响，而且保证了主Master的单点故障。    
以上就是比较常见的MySQL replication架构方案，大家可根据自己公司的具体环境来设计 ，Mysql 负载均衡可考虑用LVS或Haproxy来做，高可用HA软件我推荐Heartbeat。   
MySQL Replication的不足：如果Master主机硬件故障无法恢复，则可能造成部分未传送到slave端的数据丢失。所以大家应该根据自己目前的网络 规划，选择自己合理的Mysql架构方案，跟自己的MySQL DBA和程序员多沟涌，多备份（备份我至少会做到本地和异地双备份），多测试，数据的事是最大的事，出不得半点差错，切记切记。
