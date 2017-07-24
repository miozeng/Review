# zookeeper 命令
### ZooKeeper 常用四字命令：
ZooKeeper 支持某些特定的四字命令字母与其的交互。它们大多是查询命令，用来获取 ZooKeeper 服务的当前状态及相关信息。用户在客户端可以通过 telnet 或 nc 向 ZooKeeper 提交相应的命令

1. 可以通过命令：echo stat|nc 127.0.0.1 2181 来查看哪个节点被选择作为follower或者leader

2. 使用echo ruok|nc 127.0.0.1 2181 测试是否启动了该Server，若回复imok表示已经启动。

3. echo dump| nc 127.0.0.1 2181 ,列出未经处理的会话和临时节点。

4. echo kill | nc 127.0.0.1 2181 ,关掉server

5. echo conf | nc 127.0.0.1 2181 ,输出相关服务配置的详细信息。

6. echo cons | nc 127.0.0.1 2181 ,列出所有连接到服务器的客户端的完全的连接 / 会话的详细信息。

7. echo envi |nc 127.0.0.1 2181 ,输出关于服务环境的详细信息（区别于 conf 命令）。

8. echo reqs | nc 127.0.0.1 2181 ,列出未经处理的请求。

9. echo wchs | nc 127.0.0.1 2181 ,列出服务器 watch 的详细信息。

10. echo wchc | nc 127.0.0.1 2181 ,通过 session 列出服务器 watch 的详细信息，它的输出是一个与 watch 相关的会话的列表。

11. echo wchp | nc 127.0.0.1 2181 ,通过路径列出服务器 watch 的详细信息。它输出一个与 session 相关的路径。

### 常用命令行工具操作命令
1.ls :查看某个目录包含的所有文件    

2.ls2:查看某个目录包含的所有文件，与ls不同的是它查看到time、version等信息

3.create:创建znode，并设置初始内容 eg：create /test "hello" 

4.get: 获取znode的数据 eg: get /test

5.set:修改znode内容 eg:set /test "mio"

6.delete:删除znode eg:delete /test

7.quit:退出

### API

ZooKeeper API 共包含 5 个包，分别为： 
org.apache.zookeeper     
org.apache.zookeeper.data      
org.apache.zookeeper.server    
org.apache.zookeeper.server.quorum    
org.apache.zookeeper.server.upgrade     
其中 org.apache.zookeeper 包含 ZooKeeper 类，它我们编程时最常用的类文件。

Zookeeper类提供了如下图所示的几类主要方法    
![image]()
http://www.cnblogs.com/wuxl360/p/5817524.html 拿里面的图片

Zookeeper API的使用     
``` java
 public class demo {
     // 会话超时时间，设置为与系统默认时间一致
     private static final int SESSION_TIMEOUT=30000;
     // 创建 ZooKeeper 实例
     ZooKeeper zk;
    // 创建 Watcher 实例
    Watcher wh=new Watcher(){
            public void process(org.apache.zookeeper.WatchedEvent event)
            {
                    System.out.println(event.toString());
           }
     };

   

    // 初始化 ZooKeeper 实例
     private void createZKInstance() throws IOException
     {             
           zk=new ZooKeeper("localhost:2181",demo.SESSION_TIMEOUT,this.wh);
          
     }
 

    private void ZKOperations() throws IOException,InterruptedException,KeeperException
    {
            System.out.println("/n1. 创建 ZooKeeper 节点 (znode ： zoo2, 数据： myData2 ，权限： OPEN_ACL_UNSAFE ，节点类型： Persistent");
            zk.create("/zoo2","myData2".getBytes(), Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);

            System.out.println("/n2. 查看是否创建成功： ");
            System.out.println(new String(zk.getData("/zoo2",false,null)));
            System.out.println("/n3. 修改节点数据 ");
            zk.setData("/zoo2", "shenlan211314".getBytes(), -1);
            System.out.println("/n4. 查看是否修改成功： ");
            System.out.println(new String(zk.getData("/zoo2", false, null)));
            System.out.println("/n5. 删除节点 ");
            zk.delete("/zoo2", -1);
            System.out.println("/n6. 查看节点是否被删除： ");
            System.out.println(" 节点状态： ["+zk.exists("/zoo2", false)+"]");
     }
    

     private void ZKClose() throws  InterruptedException
     {
            zk.close();
     }

     public static void main(String[] args) throws IOException,InterruptedException,KeeperException {
            demo dm=new demo();
            dm.createZKInstance( );
            dm.ZKOperations();
           dm.ZKClose();
     }
}
``` 


### ZooKeeper示例
假设一组服务器，用于为客户端提供一些服务。我们希望每个客户端都能够能够找到其中一台服务器，使其能够使用这些服务，挑战之一就是维护这组服务器 列表。这组服务器的成员列表明显不能存在网络中的单个节点上，因为如果那个节点发生故障，就意味着是整个系统的故障（我们希望这个列表有很高的可用性）。 假设我们有了一个可靠的方法解决了这个成员列表的存储问题。如果其中一台服务器出现故障，我们仍然需要解决如何从服务器成员列表中将它删除的问题。某个进 程需要负责删除故障服务器，但注意不能由故障服务器自己来完成，因为故障服务器已经不再运行。

我们所描述的不是一个被动的分布式数据结构，而是一个主动的、能够在某个外部事件发生时修改数据项状态的数据结构。ZooKeeper提供这种服务，所以让我们看看如何使用它来实现这种众所周知的组成员管理应用。

1.创建组
``` java
package org.zk;

public class CreateGroup implements Watcher{
    private static final int SESSION_TIMEOUT=5000;
    
    private ZooKeeper zk;
    private CountDownLatch connectedSignal=new CountDownLatch(1);
    
    //客 户端已经与ZooKeeper建立连接后，Watcher的process()方法会被调用
    @Override
    public void process(WatchedEvent event) {
    //我们通过调用CountDownLatch的countDown()方法来递减它的计数器。锁存器(latch)被创建时带有一个值为1的计数器，用于表示在它释放所有等待线程之前需要发生的事件数。
    //在调用一欢countDown()方法之后，计数器的值变为0，则await()方法返回
        if(event.getState()==KeeperState.SyncConnected){
            connectedSignal.countDown();
        }
    }
 
    private void close() throws InterruptedException {
        zk.close();
    }

    private void create(String groupName) throws KeeperException, InterruptedException {
        String path="/"+groupName;
        if(zk.exists(path, false)== null){
            zk.create(path, null/*data*/, Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
        }
        System.out.println("Created:"+path);
    } 

   //方法实例化了一个新的ZooKeeper类的对象
    private void connect(String hosts) throws IOException, InterruptedException {
        zk = new ZooKeeper(hosts, SESSION_TIMEOUT, this);
        connectedSignal.await();
    }
    
       
    public static void main(String[] args) throws IOException, InterruptedException, KeeperException {
        CreateGroup createGroup = new CreateGroup();
        createGroup.connect(args[0]);
        createGroup.create(args[1]);
        createGroup.close();
    }

}
``` 


用于等待建立与ZooKeeper连接的辅助类
``` java
public class ConnectionWatcher implements Watcher{
    private static final int SESSION_TIMEOUT=5000;
    
    protected ZooKeeper zk;
    CountDownLatch connectedSignal=new CountDownLatch(1);
    public void connect(String host) throws IOException, InterruptedException{
        zk=new ZooKeeper(host, SESSION_TIMEOUT, this);
        connectedSignal.await();
    }
    @Override
    public void process(WatchedEvent event) {
        if(event.getState()==KeeperState.SyncConnected){
            connectedSignal.countDown();
        }
    }
    public void close() throws InterruptedException{
        zk.close();
    }

}
``` 

加入组
``` java
public class JoinGroup extends ConnectionWatcher{
    public void join(String groupName,String memberName) throws KeeperException, InterruptedException{
        String path="/"+groupName+"/"+memberName;
        String createdPath=zk.create(path, null, Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL);
        System.out.println("Created:"+createdPath);
    }
    public static void main(String[] args) throws InterruptedException, IOException, KeeperException {
        JoinGroup joinGroup = new JoinGroup();
        joinGroup.connect(args[0]);
        joinGroup.join(args[1], args[2]);
        
        //stay alive until process is killed or thread is interrupted
        Thread.sleep(Long.MAX_VALUE);
    }
}

``` 

列出组成员
也是extends ConnectionWatcher 并添加以下方法
``` java
 public void list(String groupNmae) throws KeeperException, InterruptedException{
        String path ="/"+groupNmae;
        try {
            List<String> children = zk.getChildren(path, false);
            if(children.isEmpty()){
                System.out.printf("No memebers in group %s\n",groupNmae);
                System.exit(1);
            }
            for(String child:children){
                System.out.println(child);
            }
        } catch (KeeperException.NoNodeException e) {
            System.out.printf("Group %s does not exist \n", groupNmae);
            System.exit(1);
        } 
    }
``` 


删除组成员
也是extends ConnectionWatcher 并添加以下方法
``` java
   public void delete(String groupName) throws InterruptedException, KeeperException{
        String path="/"+groupName;
        List<String> children;
        try {
            children = zk.getChildren(path, false);
            for(String child:children){
                zk.delete(path+"/"+child, -1);            
            }
            zk.delete(path, -1);
        } catch (KeeperException.NoNodeException e) {
            System.out.printf("Group %s does not exist\n", groupName);
            System.exit(1);
        }    
    }
``` 
下面来看如何删除一个组。ZooKeeper类提供了一个delete()方法，该方法有两个参数：

1. 路径

2. 版本号

如果所提供的版本号与znode的版本号一致，ZooKeeper会删除这个znode。这是一种乐观的加锁机制，使客户端能够检测出对znode的修改冲突。通过将版本号设置为-1，可以绕过这个版本检测机制，不管znode的版本号是什么而直接将其删除
。ZooKeeper不支持递归的删除操作，因此在删除父节点之前必须先删除子节点。




