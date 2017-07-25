# zookeeper应用
这一节主要是讲zookeeper的应用场景。
### 配置服务
使用ZooKeeper中的观察机制，可以建立一个活跃的配置服务，使那些感兴趣的客户端能够获得配置信息修改的通知。   
下面来编写一个这样的服务。我们通过两个假设来简化所需实现的服务（稍加修改就可以取消这两个假设）。    
第一，我们唯一需要存储的配置数据是字符串，关键字是znode的路径，因此我们在每个znode上存储了一个键／值对。   
第二，在任何时候只有一个客户端会执行更新操作。

``` java
public class ActiveKeyValueStore extends ConnectionWatcher {
    private static final Charset CHARSET=Charset.forName("UTF-8");
    public void write(String path,String value) throws KeeperException, InterruptedException {
    //exists操作来检测znode是否存在
        Stat stat = zk.exists(path, false);
        if(stat==null){
        //写
            zk.create(path, value.getBytes(CHARSET),Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
        }else{
            zk.setData(path, value.getBytes(CHARSET),-1);
        }
    }
    public String read(String path,Watcher watch) throws KeeperException, InterruptedException{
       //读（路径，观察对象，Stat对象）
      //Stat对象由getData()方法返回的值填充，用来将信息回传给调用者。
       //通过这个方法，调用者可以获得一个znode的数据和元数据，但在这个例子中，由于我们对元数据不感兴趣，因此将Stat参数设为null。
       byte[] data = zk.getData(path, watch, null);
        return new String(data,CHARSET);
        
    }
    
}

``` 

观察板
``` java
public class ConfigWatcher implements Watcher{
    private ActiveKeyValueStore store;

    @Override
    public void process(WatchedEvent event) {
        if(event.getType()==EventType.NodeDataChanged){
            try{
                dispalyConfig();
            }catch(InterruptedException e){
                System.err.println("Interrupted. exiting. ");
                Thread.currentThread().interrupt();
            }catch(KeeperException e){
                System.out.printf("KeeperException锛?s. Exiting.\n", e);
            }
            
        }
        
    }
    public ConfigWatcher(String hosts) throws IOException, InterruptedException {
        store=new ActiveKeyValueStore();
        store.connect(hosts);
    }
    public void dispalyConfig() throws KeeperException, InterruptedException{
        String value=store.read(ConfigUpdater.PATH, this);
        System.out.printf("Read %s as %s\n",ConfigUpdater.PATH,value);
    }

    public static void main(String[] args) throws IOException, InterruptedException, KeeperException {
        ConfigWatcher configWatcher = new ConfigWatcher(args[0]);
        configWatcher.dispalyConfig();
        //stay alive until process is killed or Thread is interrupted
        Thread.sleep(Long.MAX_VALUE);
    }
}

``` 


### 可恢复的ZooKeeper应用
在Java API中的每一个ZooKeeper操作都在其throws子句中声明了两种类型的异常，分别是InterruptedException和KeeperException。    
#### （一）InterruptedException异常

如果操作被中断，则会有一个InterruptedException异常被抛出。在Java语言中有一个取消阻塞方法的标准机制，即针对存在阻塞方法的线程调用interrupt()。一个成功的取消操作将产生一个InterruptedException异常。

ZooKeeper也遵循这一机制，因此你可以使用这种方法来取消一个ZooKeeper操作。使用了ZooKeeper的类或库通常会传播 InterruptedException异常，使客户端能够取消它们的操作。InterruptedException异常并不意味着有故障，而是表明相应的操作已经被取消，所以在配置服务的示例中，可以通过传播异常来中止应用程序的运行。

####  （二）KeeperException异常

(1) 如果ZooKeeper服务器发出一个错误信号或与服务器存在通信问题，抛出的则是KeeperException异常。

①针对不同的错误情况，KeeperException异常存在不同的子类。

例如:　KeeperException.NoNodeException是KeeperException的一个子类，如果你试图针对一个不存在的znode执行操作，抛出的则是该异常。

②每一个KeeperException异常的子类都对应一个关于错误类型信息的代码。

例如:　KeeperException.NoNodeException异常的代码是KeeperException.Code.NONODE

(2) 有两种方法被用来处理KeeperException异常：

①捕捉KeeperException异常，并且通过检测它的代码来决定采取何种补救措施；

②另一种是捕捉等价的KeeperException子类，并且在每段捕捉代码中执行相应的操作。

(3) KeeperException异常分为三大类

① 状态异常 

当一个操作因不能被应用于znode树而导致失败时，就会出现状态异常。状态异常产生的原因通常是在同一时间有另外一个进程正在修改znode。例如，如果一个znode先被另外一个进程更新了，根据版本号执行setData操作的进程就会失败，并收到一个KeeperException.BadVersionException异常，这是因为版本号不匹配。程序员通常都知道这种冲突总是存在的，也都会编写代码来进行处理。

一些状态异常会指出程序中的错误，例如KeeperException.NoChildrenForEphemeralsException异常，试图在短暂znode下创建子节点时就会抛出该异常。

② 可恢复异常

可恢复的异常是指那些应用程序能够在同一个ZooKeeper会话中恢复的异常。一个可恢复的异常是通过KeeperException.ConnectionLossException来表示的，它意味着已经丢失了与ZooKeeper的连接。ZooKeeper会尝试重新连接，并且在大多数情况下重新连接会成功，并确保会话是完整的。

但是ZooKeeper不能判断与KeeperException.ConnectionLossException异常相关的操作是否成功执行。这种情况就是部分失败的一个例子。这时程序员有责任来解决这种不确定性，并且根据应用的情况来采取适当的操作。在这一点上，就需要对“幂等”(idempotent)操作和“非幂等”(Nonidempotent)操作进行区分。幂等操作是指那些一次或多次执行都会产生相同结果的操作，例如读请求或无条件执行的setData操作。对于幂等操作，只需要简单地进行重试即可。对于非幂等操作，就不能盲目地进行重试，因为它们多次执行的结果与一次执行是完全不同的。程序可以通过在znode的路径和它的数据中编码信息来检测是否非幂等操怍的更新已经完成。

③不可恢复的异常 

在某些情况下，ZooKeeper会话会失效——也许因为超时或因为会话被关闭，两种情况下都会收到KeeperException.SessionExpiredException异常，或因为身份验证失败，KeeperException.AuthFailedException异常。无论上述哪种情况，所有与会话相关联的短暂znode都将丢失，因此应用程序需要在重新连接到ZooKeeper之前重建它的状态。


``` java
public void write(String path,String value) throws InterruptedException, KeeperException{
        int retries=0;
        while(true){
            try {
                Stat stat = zk.exists(path, false);
                if(stat==null){
                    zk.create(path, value.getBytes(CHARSET),Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
                }else{
                    zk.setData(path, value.getBytes(CHARSET),stat.getVersion());
                }
            } catch (KeeperException.SessionExpiredException e) {
                throw e;
            } catch (KeeperException e) {
                if(retries++==MAX_RETRIES){
                    throw e;
                }
                //sleep then retry
                TimeUnit.SECONDS.sleep(RETRY_PERIOD_SECONDS);
            }
        }
    }
    
``` 
在该类中，对前面的write()进行了修改,该版本的wirte()能够循环执行重试。其中设置了重试的最大次数MAX_RETRIES和两次重试之间的间隔RETRY_PERIOD_SECONDS.


### 锁服务
#### 分布式锁概述
分布式锁在一组进程之间提供了一种互斥机制。在任何时刻，在任何时刻只有一个进程可以持有锁。分布式锁可以在大型分布式系统中实现领导者选举，在任何时间点，持有锁的那个进程就是系统的领导者
#### zookeeper实现
实现正确地实现一个分布式锁是一件棘手的事，因为很难对所有类型的故障都进行正确的解释处理。ZooKeeper带有一个 JavaWriteLock，客户端可以很方便地使用它。更多分布式数据结构和协议例如“屏障”(bafrier)、队列和两阶段提交协议。有趣的是它们 都是同步协议，即使我们使用异步ZooKeeper基本操作（如通知）来实现它们。使用ZooKeeper可以实现很多不同的分布式数据结构和协 议，ZooKeeper网站(http://hadoop.apache.org/zookeeper/)提供了一些用于实现分布式数据结构和协议的伪代码。ZooKeeper本身也带有一些棕准方法的实现，放在安装位置下的recipes目录中。
    
```  java
public class DistributedLock implements Lock, Watcher{
    private ZooKeeper zk;
    private String root = "/locks";//根
    private String lockName;//竞争资源的标志
    private String waitNode;//等待前一个锁
    private String myZnode;//当前锁
    private CountDownLatch latch;//计数器
    private int sessionTimeout = 30000;
    private List<Exception> exception = new ArrayList<Exception>();
     
    /**
     * 创建分布式锁,使用前请确认config配置的zookeeper服务可用
     * @param config 127.0.0.1:2181
     * @param lockName 竞争资源标志,lockName中不能包含单词lock
     */
    public DistributedLock(String config, String lockName){
        this.lockName = lockName;
        // 创建一个与服务器的连接
         try {
            zk = new ZooKeeper(config, sessionTimeout, this);
            Stat stat = zk.exists(root, false);
            if(stat == null){
                // 创建根节点
                zk.create(root, new byte[0], ZooDefs.Ids.OPEN_ACL_UNSAFE,CreateMode.PERSISTENT);
            }
        } catch (IOException e) {
            exception.add(e);
        } catch (KeeperException e) {
            exception.add(e);
        } catch (InterruptedException e) {
            exception.add(e);
        }
    }
 
    /**
     * zookeeper节点的监视器
     */
    public void process(WatchedEvent event) {
        if(this.latch != null) { 
            this.latch.countDown(); 
        }
    }
     
    public void lock() {
        if(exception.size() > 0){
            throw new LockException(exception.get(0));
        }
        try {
            if(this.tryLock()){
                System.out.println("Thread " + Thread.currentThread().getId() + " " +myZnode + " get lock true");
                return;
            }
            else{
                waitForLock(waitNode, sessionTimeout);//等待锁
            }
        } catch (KeeperException e) {
            throw new LockException(e);
        } catch (InterruptedException e) {
            throw new LockException(e);
        }
    }
 
    public boolean tryLock() {
        try {
            String splitStr = "_lock_";
            if(lockName.contains(splitStr))
                throw new LockException("lockName can not contains \\u000B");
            //创建临时子节点
            myZnode = zk.create(root + "/" + lockName + splitStr, new byte[0], ZooDefs.Ids.OPEN_ACL_UNSAFE,CreateMode.EPHEMERAL_SEQUENTIAL);
            System.out.println(myZnode + " is created ");
            //取出所有子节点
            List<String> subNodes = zk.getChildren(root, false);
            //取出所有lockName的锁
            List<String> lockObjNodes = new ArrayList<String>();
            for (String node : subNodes) {
                String _node = node.split(splitStr)[0];
                if(_node.equals(lockName)){
                    lockObjNodes.add(node);
                }
            }
            Collections.sort(lockObjNodes);
            System.out.println(myZnode + "==" + lockObjNodes.get(0));
            if(myZnode.equals(root+"/"+lockObjNodes.get(0))){
                //如果是最小的节点,则表示取得锁
                return true;
            }
            //如果不是最小的节点，找到比自己小1的节点
            String subMyZnode = myZnode.substring(myZnode.lastIndexOf("/") + 1);
            waitNode = lockObjNodes.get(Collections.binarySearch(lockObjNodes, subMyZnode) - 1);
        } catch (KeeperException e) {
            throw new LockException(e);
        } catch (InterruptedException e) {
            throw new LockException(e);
        }
        return false;
    }
 
    public boolean tryLock(long time, TimeUnit unit) {
        try {
            if(this.tryLock()){
                return true;
            }
            return waitForLock(waitNode,time);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }
 
    private boolean waitForLock(String lower, long waitTime) throws InterruptedException, KeeperException {
        Stat stat = zk.exists(root + "/" + lower,true);
        //判断比自己小一个数的节点是否存在,如果不存在则无需等待锁,同时注册监听
        if(stat != null){
            System.out.println("Thread " + Thread.currentThread().getId() + " waiting for " + root + "/" + lower);
            this.latch = new CountDownLatch(1);
            this.latch.await(waitTime, TimeUnit.MILLISECONDS);
            this.latch = null;
        }
        return true;
    }
 
    public void unlock() {
        try {
            System.out.println("unlock " + myZnode);
            zk.delete(myZnode,-1);
            myZnode = null;
            zk.close();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (KeeperException e) {
            e.printStackTrace();
        }
    }
 
    public void lockInterruptibly() throws InterruptedException {
        this.lock();
    }
 
    public Condition newCondition() {
        return null;
    }
     
    public class LockException extends RuntimeException {
        private static final long serialVersionUID = 1L;
        public LockException(String e){
            super(e);
        }
        public LockException(Exception e){
            super(e);
        }
    }
 
}
    
``` 

### BooKeeper概述
BooKeeper具有副本功能，目的是提供可靠的日志记录。在BooKeeper中，服务器被称为账本（Bookies），在账本之中有不同的账户（Ledgers），每一个账户由一条条记录（Entry）组成。如果使用普通的磁盘存储日志数据，那么日志数据可能遭到破坏，当磁盘发生故障的时候，日志也可能被丢失。BooKeeper为每一份日志提供了分布式的存储，并采用了大多数（quorum，相对于全体）的概念。也就是说，只要集群中的大多数机器可用，那么该日志一直有效。

BooKeeper通过客户端进行操作，客户端可以对BooKeeper进行添加账户、打开账户、添加账户记录、读取账户记录等操作。另外，BooKeeper的服务依赖于ZooKeeper，可以说BooKeeper依赖于ZooKeeper的一致性及其分布式特点，在其之上提供另外一种可靠性服务

具体实例不讲了



