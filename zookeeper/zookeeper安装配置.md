### Zookeeper安装方式有三种，单机模式和集群模式以及伪集群模式。
. 单机模式：Zookeeper只运行在一台服务器上，适合测试环境；
. 伪集群模式：就是在一台物理机上运行多个Zookeeper 实例；
. 集群模式：Zookeeper运行于一个集群上，适合生产环境，这个计算机集群被称为一个“集合体”（ensemble）

### 单机模式
zookeeper目录下的conf子目录, 创建zoo.cfg
``` java
#zookeeper中使用的基本时间单位, 毫秒值.
tickTime=2000  
#数据目录. 可以是任意目录.
dataDir=/Users/apple/zookeeper/data  
#log目录, 同样可以是任意目录. 如果没有设置该参数, 将使用和dataDir相同的设置.
dataLogDir=/Users/apple/zookeeper/logs 
#监听client连接的端口号.
clientPort=4180
```


### Zookeeper的伪集群模式
Zookeeper不但可以在单机上运行单机模式Zookeeper，而且可以在单机模拟集群模式 Zookeeper的运行，也就是将不同节点运行在同一台机器。

在一台机器上部署了3个server，需要注意的是在集群为分布式模式下我们使用的每个配置文档模拟一台机器，也就是说单台机器及上运行多个Zookeeper实例。但是，必须保证每个配置文档的各个端口号不能冲突，除了clientPort不同之外，dataDir也不同。
另外，还要在dataDir所对应的目录中创建myid文件来指定对应的Zookeeper服务器实例。

下面是我所配置的集群伪分布模式，分别通过zoo1.cfg、zoo2.cfg、zoo3.cfg来模拟由三台机器的Zookeeper集群,代码清单 zoo1.cfg如下:
``` java
tickTime=2000
#zookeeper集群中的包含多台server, 其中一台为leader, 集群中其余的server为follower. initLimit参数配置初始化连接时, 
#follower和leader之间的最长心跳时间. 此时该参数设置为5, 说明时间限制为5倍tickTime, 即5*2000=10000ms=10s.
initLimit=5
#该参数配置leader和follower之间发送消息, 请求和应答的最大时间长度. 此时该参数设置为5, 说明时间限制为5倍tickTime, 即10000ms.
syncLimit=5
dataDir=/usr/local/zk/data_1
clientPort=2181
dataLogDir=/usr/local/zk/logs_1
#server.X=A:B:C 其中X是一个数字, 表示这是第几号server. A是该server所在的IP地址. 
#B配置该server和集群中的leader交换消息所使用的端口. C配置选举leader时所使用的端口. 由于配置的是伪集群模式, 所以各个server的B, C参数必须不同.
server.0=localhost:2287:3387
server.1=localhost:2288:3388
server.2=localhost:2289:3389
``

在之前设置的dataDir中新建myid文件, 写入一个数字, 该数字表示这是第几号server. 该数字必须和zoo.cfg文件中的server.X中的X一一对应.
/Users/apple/zookeeper0/data/myid文件中写入0, /Users/apple/zookeeper1/data/myid文件中写入1, /Users/apple/zookeeper2/data/myid文件中写入2.
` 
服务启动
``` java
zkServer.sh start zoo1.sh
zkServer.sh start zoo2.sh
zkServer.sh start zoo3.sh
``` 

### Zookeeper的集群
为了获得可靠地Zookeeper服务，用户应该在一个机群上部署Zookeeper。只要机群上大多数的Zookeeper服务启动了，那么总的 Zookeeper服务将是可用的。集群的配置方式，和前两种类似，同样需要进行环境变量的配置。
#### 在dataDir(/usr/local/zk/data)目录创建myid文件

Server0机器的内容为：43
Server1机器的内容为：47
Server2机器的内容为：48

#### 在每台机器上conf/zoo.cf配置文件的参数设置 相同

``` java
tickTime=2000  
initLimit=5  
syncLimit=2  
dataDir=/home/zookeeper/data  
dataLogDir=/home/zookeeper/logs  
clientPort=4180
server.43=10.1.39.43:2888:3888
server.47=10.1.39.47:2888:3888  
server.48=10.1.39.48:2888:3888
``` 

示例中部署了3台zookeeper server, 分别部署在10.1.39.43, 10.1.39.47, 10.1.39.48上. 需要注意的是, 各server的dataDir目录下的myid文件中的数字必须不同.

10.1.39.43 server的myid为43, 10.1.39.47 server的myid为47, 10.1.39.48 server的myid为48.

更多配置：       
minSessionTimeout和maxSessionTimeout   
即最小的会话超时和最大的会话超时时间。在默认情况下，minSession=2*tickTime；maxSession=20*tickTime。
maxClientCnxns     
这个操作将限制连接到Zookeeper的客户端数量，并限制并发连接的数量，通过IP来区分不同的客户端。此配置选项可以阻止某些类别的Dos攻击。将他设置为零或忽略不进行设置将会取消对并发连接的限制     







