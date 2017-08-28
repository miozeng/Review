### 1. 基础概念
ActiveMQ：是Apache出品，最流行的，能力强劲的开源消息总线。是一个完全支持JMS1.1和J2EE 1.4规范的 JMS Provider实现。带有易于在充分支持JMS 1.1和1.4使用J2EE企业集成模式和许多先进的功能。
JMS（Java消息服务）：是一个Java平台中关于面向消息中间件（MOM）的API，用于在两个应用程序之间，或分布式系统中发送消息，进行异步通信。
### 2. JMS消息模式
1) 点对点或队列模式
  每个消息只能有一个消费者。消息的生产者和消费者之间没有时间上的相关性，无论消费者在生产者发送消息的时候是否处于运行状态，它都可以提取消息。

2) Pub/Sub 发布/订阅模式
每个消息可以有多个消费者。生产者和消费者之间有时间上的相关性。订阅一个主题的消费者只能消费自它订阅之后发布的消息。
### 3. Broker节点
代表一个运行MQ的节点。
### 4. Transport传输方式
ActiveMQ目前支持的Transport有：VM Transport、TCP Transport、NIO Transport、SSL Transport、Peer Transport、UDP Transport、Multicast Transport、HTTP and HTTPS Transport、WebSockets Transport、Failover Transport、Fanout Transport、Discovery Transport、ZeroConf Transport等。
1) VM Transport：允许客户端和Broker直接在VM内部通信，采用的连接不是Socket连接，而是直接的方法调用，从而避免了网络传输的开销。应用场景也仅限于Broker和客户端在同一JVM环境下。

2) TCP Transport：客户端通过TCP Socket连接到远程Broker。配置语法：   
tcp://hostname:port?transportOptions   

3) HTTP and HTTPS Transport：允许客户端使用REST或者Ajax的方式进行连接。这意味着可以直接使用Javascript向ActiveMQ发送消息。   

4) WebSockets Transport：允许客户端通过HTML5标准的WebSockets方式连接到Broker。

5) Failover Transport：青龙系统MQ采用的就是这种连接方式。这种方式具备自动重新连接的机制，工作在其他Transport的上层，用于建立可靠的传输。允许配置任意多个的URI，该机制将会自动选择其中的一个URI来尝试连接。配置语法：
failover:(tcp://localhost:61616,tcp://localhost:61617,.....)?transportOptions

6) Fanout Transport：主要适用于生产消息发向多个代理。如果多个代理出现环路，可能造成消费者接收重复的消息。所以，使用该协议时，最好将消息发送给多个不相连接的代理。

### 5. Persistence持久化存储
1) AMQ Message Store
ActiveMQ 5.0 的缺省持久化存储方式。

2) Kaha Persistence
这是一个专门针对消息持久化的解决方案。它对典型的消息使用模式进行了优化。

3) JDBC Persistence
目前支持的数据库有：Apache Derby, Axion, DB2, HSQL, Informix, MaxDB, MySQL, Oracle, Postgresql, SQLServer, Sybase。

4) Disable Persistence
不应用持久化存储。

### 6. 集群方案
#### 1. Master / Slave  
1.1. Pure Master Slave  
无单点故障；  
不需要依赖共享文件系统或是共享数据库，使用 KahaDB的方式持久化存储；   
一个Master只能带一个Slave；  
Master工作期间，会将消息状况自动同步到Slave；  
Master一旦崩溃，Slave自动接替其工作，已发送并尚未消费的消息继续有效；  
Slave接手后，必须停止Slave才能重启先前的Master；  

1.2. Shared File System Master Slave 

1.3. JDBC Master Slave
配置上，不存在Master和Slave的区分，多个共享数据源的Broker构成JDBC Master Slave；  
首先抢到资源（数据库锁）的Broker成为Master，其他Broker定期尝试抢占资源；  
一旦Master崩溃，其他Broker抢占资源，最终只有一台抢到，立刻成为Master，之前的Master即便重启成功，也只能作为Slave等待；  

### 7.特性
1、 多种语言和协议编写客户端。语言： Java、C、C++、C#、Ruby、Perl、Python、PHP。应用协议：OpenWire、Stomp REST、WS Notification、XMPP、AMQP   

2、完全支持JMS1.1和J2EE 1.4规范 （持久化，XA消息，事务)   

3、对Spring的支持，ActiveMQ可以很容易内嵌到使用Spring的系统里面去，而且也支持Spring2.0的特性   

4、通过了常见J2EE服务器（如 Geronimo、JBoss 4、GlassFish、WebLogic)的测试，其中通过JCA 1.5 resource adaptors的配置，可以让ActiveMQ可以自动的部署到任何兼容J2EE 1.4 商业服务器上   

5、支持多种传送协议：in-VM、TCP、SSL、NIO、UDP、JGroups、JXTA   

6、支持通过JDBC和journal提供高速的消息持久化   

7、从设计上保证了高性能的集群，客户端-服务器，点对点

8、支持Ajax  

9、支持与Axis的整合  

10、可以很容易得调用内嵌JMS provider，进行测试  

###  8.实例
1、 下载ActiveMQ，下载地址：http://www.apache.org/dyn/closer.cgi?path=/activemq/apache-activemq/5.8.0/apache-activemq-5.8.0-bin.zip

2、 解压apache-activemq-5.8.0.zip即可完成ActiveMQ的安装

3、 解压后目录结构如下

+bin (windows下面的bat和unix/linux下面的sh) 启动ActiveMQ的启动服务就在这里   
+conf (activeMQ配置目录，包含最基本的activeMQ配置文件）   
+data （默认是空的）  
+docs （index,replease版本里面没有文档）   
+example （几个例子）   
+lib （activeMQ使用到的lib）  
+webapps （系统管理员控制台代码）  
+webapps-demo（系统示例代码）  
-activemq-all-5.8.0.jar (ActiveMQ的binary)  
-user-guide.html （部署指引）   
-LICENSE.txt  
-NOTICE.txt  
-README.txt  
 
其他文件就不相信介绍了，搞Java的应该都知道干什么用的。   
你可以进入bin目录，使用activemq.bat双击启动（windows用户可以选择系统位数，如果你是linux的话，就用命令行的发送去启动），如果一切顺利，你就会看见类似下面的信息：
     
如果你看到这个，那么恭喜你成功了。如果你启动看到了异常信息：   
Caused by: java.io.IOException: Failed to bind to server socket: tcp://0.0.0.0:61616?maximumConnections=1000&wireformat.maxFrameSize=104857600 due to: java.net.SocketException: Unrecognized Windows Sockets error: 0: JVM_Bind
那么我告诉你，很不幸，你的端口被占用了。接下来你大概想知道是哪个程序占用了你的端口，并kill掉该进程或服务。或者你要尝试修改ActiveMQ的默认端口61616（ActiveMQ使用的默认端口是61616），在大多数情况下，占用61616端口的是Internet Connection Sharing (ICS) 这个Windows服务，你只需停止它就可以启动ActiveMQ了。

4、 启动成功就可以访问管理员界面：http://localhost:8161/admin，默认用户名和密码admin/admin。如果你想修改用户名和密码的话，在conf/jetty-realm.properties中修改即可。   
其中在导航菜单中，Queues是队列方式消息。Topics是主题方式消息。Subscribers消息订阅监控查询。Connections可以查看链接数，分别可以查看xmpp、ssl、stomp、openwire、ws和网络链接。Network是网络链接数监控。Send可以发送消息数据。
   
5、 运行demo示例，在dos控制台输入activemq.bat xbean:../conf/activemq-demo.xml 即可启动demo示例。官方提供的user-guide.html中的access the web console中是提示输入：activemq.bat console xbean:conf/activemq-demo.xml，我用这种方式不成功。
当然你还可以用绝对的文件目录方式：activemq.bat xbean:file:D:/mq/conf/activemq-demo.xml    
如果提示conf/activemq-demo.xml没有找到，你可以尝试改变下路径，也就是去掉上面的“..”。通过http://localhost:8161/demo/ 就可以访问示例了。     

### 1、ActiviteMQ消息有3中形式

JMS 公共	点对点域	发布/订阅域
ConnectionFactory	QueueConnectionFactory	TopicConnectionFactory
Connection	QueueConnection	TopicConnection
Destination	Queue	Topic
Session	QueueSession	TopicSession
MessageProducer	QueueSender	TopicPublisher
MessageConsumer	QueueReceiver	TopicSubscriber

(1)、点对点方式（point-to-point）
点对点的消息发送方式主要建立在 Message Queue,Sender,reciever上，Message Queue 存贮消息，Sneder 发送消息，receive接收消息.具体点就是Sender Client发送Message Queue ,而 receiver Cliernt从Queue中接收消息和"发送消息已接受"到Quere,确认消息接收。消息发送客户端与接收客户端没有时间上的依赖，发送客户端可以在任何时刻发送信息到Queue，而不需要知道接收客户端是不是在运行

(2)、发布/订阅 方式（publish/subscriber Messaging）
发布/订阅方式用于多接收客户端的方式.作为发布订阅的方式，可能存在多个接收客户端，并且接收端客户端与发送客户端存在时间上的依赖。一个接收端只能接收他创建以后发送客户端发送的信息。作为subscriber ,在接收消息时有两种方法，destination的receive方法，和实现message listener 接口的onMessage 方法。

### 2、ActiviteMQ接收和发送消息基本流程
发送消息的基本步骤：  
(1)、创建连接使用的工厂类JMS ConnectionFactory   
(2)、使用管理对象JMS ConnectionFactory建立连接Connection，并启动  
(3)、使用连接Connection 建立会话Session   
(4)、使用会话Session和管理对象Destination创建消息生产者MessageSender   
(5)、使用消息生产者MessageSender发送消息   
 
消息接收者从JMS接受消息的步骤   
(1)、创建连接使用的工厂类JMS ConnectionFactory   
(2)、使用管理对象JMS ConnectionFactory建立连接Connection，并启动   
(3)、使用连接Connection 建立会话Session   
(4)、使用会话Session和管理对象Destination创建消息接收者MessageReceiver    
(5)、使用消息接收者MessageReceiver接受消息，需要用setMessageListener将MessageListener接口绑定到MessageReceiver消息接收者必须实现了MessageListener接口，需要定义onMessage事件方法。

### 8.2、 代码示例   
在代码开始，我们先建一个project，在这个project中添加依赖jar包

添加完jar包后就可以开始实际的代码工作了。
### 1、 使用JMS方式发送接收消息
消息发送者

``` java
package com.hoo.mq.jms;
 
import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.DeliveryMode;
import javax.jms.Destination;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
 
/**
 * <b>function:</b> 消息发送者
 * @author hoojo
 * @createDate 2013-6-19 上午11:26:43
 * @file MessageSender.java
 * @package com.hoo.mq.jms
 * @project ActiveMQ-5.8
 * @blog http://blog.csdn.net/IBM_hoojo
 * @email hoojo_@126.com
 * @version 1.0
 */
public class MessageSender {
 
    // 发送次数
    public static final int SEND_NUM = 5;
    // tcp 地址
    public static final String BROKER_URL = "tcp://localhost:61616";
    // 目标，在ActiveMQ管理员控制台创建 http://localhost:8161/admin/queues.jsp
    public static final String DESTINATION = "hoo.mq.queue";
    
    /**
     * <b>function:</b> 发送消息
     * @author hoojo
     * @createDate 2013-6-19 下午12:05:42
     * @param session
     * @param producer
     * @throws Exception
     */    
    public static void sendMessage(Session session, MessageProducer producer) throws Exception {
        for (int i = 0; i < SEND_NUM; i++) {
            String message = "发送消息第" + (i + 1) + "条";
            TextMessage text = session.createTextMessage(message);
            
            System.out.println(message);
            producer.send(text);
        }
    }
    
    public static void run() throws Exception {
        
        Connection connection = null;
        Session session = null;
        try {
            // 创建链接工厂
            ConnectionFactory factory = new ActiveMQConnectionFactory(ActiveMQConnection.DEFAULT_USER, ActiveMQConnection.DEFAULT_PASSWORD, BROKER_URL);
            // 通过工厂创建一个连接
            connection = factory.createConnection();
            // 启动连接
            connection.start();
            // 创建一个session会话
            session = connection.createSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
            // 创建一个消息队列
            Destination destination = session.createQueue(DESTINATION);
            // 创建消息制作者
            MessageProducer producer = session.createProducer(destination);
            // 设置持久化模式
            producer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);
            sendMessage(session, producer);
            // 提交会话
            session.commit();
            
        } catch (Exception e) {
            throw e;
        } finally {
            // 关闭释放资源
            if (session != null) {
                session.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }
    
    public static void main(String[] args) throws Exception {
        MessageSender.run();
    }
}
``` 

接受者

``` java
package com.hoo.mq.jms;
 
import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.Message;
import javax.jms.MessageConsumer;
import javax.jms.Session;
import javax.jms.TextMessage;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
 
/**
 * <b>function:</b> 消息接收者
 * @author hoojo
 * @createDate 2013-6-19 下午01:34:27
 * @file MessageReceiver.java
 * @package com.hoo.mq.jms
 * @project ActiveMQ-5.8
 * @blog http://blog.csdn.net/IBM_hoojo
 * @email hoojo_@126.com
 * @version 1.0
 */
public class MessageReceiver {
 
    // tcp 地址
    public static final String BROKER_URL = "tcp://localhost:61616";
    // 目标，在ActiveMQ管理员控制台创建 http://localhost:8161/admin/queues.jsp
    public static final String DESTINATION = "hoo.mq.queue";
    
    
    public static void run() throws Exception {
        
        Connection connection = null;
        Session session = null;
        try {
            // 创建链接工厂
            ConnectionFactory factory = new ActiveMQConnectionFactory(ActiveMQConnection.DEFAULT_USER, ActiveMQConnection.DEFAULT_PASSWORD, BROKER_URL);
            // 通过工厂创建一个连接
            connection = factory.createConnection();
            // 启动连接
            connection.start();
            // 创建一个session会话
            session = connection.createSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
            // 创建一个消息队列
            Destination destination = session.createQueue(DESTINATION);
            // 创建消息制作者
            MessageConsumer consumer = session.createConsumer(destination);
            
            while (true) {
                // 接收数据的时间（等待） 100 ms
                Message message = consumer.receive(1000 * 100);
                
                TextMessage text = (TextMessage) message;
                if (text != null) {
                    System.out.println("接收：" + text.getText());
                } else {
                    break;
                }
            }
            
            // 提交会话
            session.commit();
            
        } catch (Exception e) {
            throw e;
        } finally {
            // 关闭释放资源
            if (session != null) {
                session.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }
    
    public static void main(String[] args) throws Exception {
        MessageReceiver.run();
    }
}
``` 
 
### 2、 Queue队列方式发送点对点消息数据
发送方
``` java
package com.hoo.mq.queue;
 
import javax.jms.DeliveryMode;
import javax.jms.MapMessage;
import javax.jms.Queue;
import javax.jms.QueueConnection;
import javax.jms.QueueConnectionFactory;
import javax.jms.QueueSession;
import javax.jms.Session;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
 
/**
 * <b>function:</b> Queue 方式消息发送者
 * @author hoojo
 * @createDate 2013-6-19 下午04:34:36
 * @file QueueSender.java
 * @package com.hoo.mq.queue
 * @project ActiveMQ-5.8
 * @blog http://blog.csdn.net/IBM_hoojo
 * @email hoojo_@126.com
 * @version 1.0
 */
public class QueueSender {
    
    // 发送次数
    public static final int SEND_NUM = 5;
    // tcp 地址
    public static final String BROKER_URL = "tcp://localhost:61616";
    // 目标，在ActiveMQ管理员控制台创建 http://localhost:8161/admin/queues.jsp
    public static final String DESTINATION = "hoo.mq.queue";
    
    /**
     * <b>function:</b> 发送消息
     * @author hoojo
     * @createDate 2013-6-19 下午12:05:42
     * @param session
     * @param sender
     * @throws Exception
     */    
    public static void sendMessage(QueueSession session,javax.jms.QueueSender sender) throws Exception {
 for (int i = 0; i < SEND_NUM; i++) {
     String message = "发送消息第" + (i + 1) + "条";
            
            MapMessage map = session.createMapMessage();
            map.setString("text", message);
            map.setLong("time", System.currentTimeMillis());
            System.out.println(map);
            
            sender.send(map);
        }
    }
      public static void run() throws Exception {
        
         QueueConnection connection = null;
  QueueSession session = null;
  try {
            // 创建链接工厂
            QueueConnectionFactory factory = new ActiveMQConnectionFactory(ActiveMQConnection.DEFAULT_USER, ActiveMQConnection.DEFAULT_PASSWORD, BROKER_URL);
            // 通过工厂创建一个连接
            connection = factory.createQueueConnection();
            // 启动连接
            connection.start();
            // 创建一个session会话
            session = connection.createQueueSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
            // 创建一个消息队列
            Queue queue = session.createQueue(DESTINATION);
            // 创建消息发送者
            javax.jms.QueueSender sender = session.createSender(queue);
            // 设置持久化模式
            sender.setDeliveryMode(DeliveryMode.NON_PERSISTENT);
            sendMessage(session, sender);
            // 提交会话
            session.commit();
            
        } catch (Exception e) {
            throw e;
        } finally {
            // 关闭释放资源
            if (session != null) {
                session.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }
    
    public static void main(String[] args) throws Exception {
        QueueSender.run();
    }
}
``` 

接收方

``` java
package com.hoo.mq.queue;
 
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.Queue;
import javax.jms.QueueConnection;
import javax.jms.QueueConnectionFactory;
import javax.jms.QueueSession;
import javax.jms.Session;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
 
/**
 * <b>function:</b> 消息接收者； 依赖hawtbuf-1.9.jar
 * @author hoojo
 * @createDate 2013-6-19 下午01:34:27
 * @file MessageReceiver.java
 * @package com.hoo.mq.queue
 * @project ActiveMQ-5.8
 * @blog http://blog.csdn.net/IBM_hoojo
 * @email hoojo_@126.com
 * @version 1.0
 */
public class QueueReceiver {
 
    // tcp 地址
    public static final String BROKER_URL = "tcp://localhost:61616";
    // 目标，在ActiveMQ管理员控制台创建 http://localhost:8161/admin/queues.jsp
    public static final String TARGET = "hoo.mq.queue";
    
    
    public static void run() throws Exception {
        
        QueueConnection connection = null;
        QueueSession session = null;
        try {
            // 创建链接工厂
            QueueConnectionFactory factory = new ActiveMQConnectionFactory(ActiveMQConnection.DEFAULT_USER, ActiveMQConnection.DEFAULT_PASSWORD, BROKER_URL);
            // 通过工厂创建一个连接
            connection = factory.createQueueConnection();
            // 启动连接
            connection.start();
            // 创建一个session会话
            session = connection.createQueueSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
            // 创建一个消息队列
            Queue queue = session.createQueue(TARGET);
            // 创建消息制作者
            javax.jms.QueueReceiver receiver = session.createReceiver(queue);
            
            receiver.setMessageListener(new MessageListener() { 
                public void onMessage(Message msg) { 
                    if (msg != null) {
                        MapMessage map = (MapMessage) msg;
                        try {
                            System.out.println(map.getLong("time") + "接收#" + map.getString("text"));
                        } catch (JMSException e) {
                            e.printStackTrace();
                        }
                    }
                } 
            }); 
            // 休眠100ms再关闭
            Thread.sleep(1000 * 100); 
            
            // 提交会话
            session.commit();
            
        } catch (Exception e) {
            throw e;
        } finally {
            // 关闭释放资源
            if (session != null) {
                session.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }
    
    public static void main(String[] args) throws Exception {
        QueueReceiver.run();
    }
}
```  

### 3、 Topic主题发布和订阅消息

消息发送方

``` java
package com.hoo.mq.topic;
 
import javax.jms.DeliveryMode;
import javax.jms.MapMessage;
import javax.jms.Session;
import javax.jms.Topic;
import javax.jms.TopicConnection;
import javax.jms.TopicConnectionFactory;
import javax.jms.TopicPublisher;
import javax.jms.TopicSession;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
 
 
/**
 * <b>function:</b> Queue 方式消息发送者
 * @author hoojo
 * @createDate 2013-6-19 下午04:34:36
 * @file QueueSender.java
 * @package com.hoo.mq.topic
 * @project ActiveMQ-5.8
 * @blog http://blog.csdn.net/IBM_hoojo
 * @email hoojo_@126.com
 * @version 1.0
 */
public class TopicSender {
    
    // 发送次数
    public static final int SEND_NUM = 5;
    // tcp 地址
    public static final String BROKER_URL = "tcp://localhost:61616";
    // 目标，在ActiveMQ管理员控制台创建 http://localhost:8161/admin/queues.jsp
    public static final String DESTINATION = "hoo.mq.topic";
    
    /**
     * <b>function:</b> 发送消息
     * @author hoojo
     * @createDate 2013-6-19 下午12:05:42
     * @param session 会话
     * @param publisher 发布者
     * @throws Exception
     */    
    public static void sendMessage(TopicSession session, TopicPublisher publisher) throws Exception {
        for (int i = 0; i < SEND_NUM; i++) {
            String message = "发送消息第" + (i + 1) + "条";
            
            MapMessage map = session.createMapMessage();
            map.setString("text", message);
            map.setLong("time", System.currentTimeMillis());
            System.out.println(map);
            
            publisher.send(map);
        }
    }
    
    public static void run() throws Exception {
        
        TopicConnection connection = null;
        TopicSession session = null;
        try {
            // 创建链接工厂
            TopicConnectionFactory factory = new ActiveMQConnectionFactory(ActiveMQConnection.DEFAULT_USER, ActiveMQConnection.DEFAULT_PASSWORD, BROKER_URL);
            // 通过工厂创建一个连接
            connection = factory.createTopicConnection();
            // 启动连接
            connection.start();
            // 创建一个session会话
            session = connection.createTopicSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
            // 创建一个消息队列
            Topic topic = session.createTopic(DESTINATION);
            // 创建消息发送者
            TopicPublisher publisher = session.createPublisher(topic);
            // 设置持久化模式
            publisher.setDeliveryMode(DeliveryMode.NON_PERSISTENT);
            sendMessage(session, publisher);
            // 提交会话
            session.commit();
            
        } catch (Exception e) {
            throw e;
        } finally {
            // 关闭释放资源
            if (session != null) {
                session.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }
    
    public static void main(String[] args) throws Exception {
        TopicSender.run();
    }
}
```

接收方

``` java
package com.hoo.mq.topic;
 
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.Session;
import javax.jms.Topic;
import javax.jms.TopicConnection;
import javax.jms.TopicConnectionFactory;
import javax.jms.TopicSession;
import javax.jms.TopicSubscriber;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
 
/**
 * <b>function:</b> 消息接收者； 依赖hawtbuf-1.9.jar
 * @author hoojo
 * @createDate 2013-6-19 下午01:34:27
 * @file MessageReceiver.java
 * @package com.hoo.mq.topic
 * @project ActiveMQ-5.8
 * @blog http://blog.csdn.net/IBM_hoojo
 * @email hoojo_@126.com
 * @version 1.0
 */
public class TopicReceiver {
 
    // tcp 地址
    public static final String BROKER_URL = "tcp://localhost:61616";
    // 目标，在ActiveMQ管理员控制台创建 http://localhost:8161/admin/queues.jsp
    public static final String TARGET = "hoo.mq.topic";
    
    
    public static void run() throws Exception {
        
        TopicConnection connection = null;
        TopicSession session = null;
        try {
            // 创建链接工厂
            TopicConnectionFactory factory = new ActiveMQConnectionFactory(ActiveMQConnection.DEFAULT_USER, ActiveMQConnection.DEFAULT_PASSWORD, BROKER_URL);
            // 通过工厂创建一个连接
            connection = factory.createTopicConnection();
            // 启动连接
            connection.start();
            // 创建一个session会话
            session = connection.createTopicSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
            // 创建一个消息队列
            Topic topic = session.createTopic(TARGET);
            // 创建消息制作者
            TopicSubscriber subscriber = session.createSubscriber(topic);
            
            subscriber.setMessageListener(new MessageListener() { 
                public void onMessage(Message msg) { 
                    if (msg != null) {
                        MapMessage map = (MapMessage) msg;
                        try {
                            System.out.println(map.getLong("time") + "接收#" + map.getString("text"));
                        } catch (JMSException e) {
                            e.printStackTrace();
                        }
                    }
                } 
            }); 
            // 休眠100ms再关闭
            Thread.sleep(1000 * 100); 
            
            // 提交会话
            session.commit();
            
        } catch (Exception e) {
            throw e;
        } finally {
            // 关闭释放资源
            if (session != null) {
                session.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }
    
    public static void main(String[] args) throws Exception {
        TopicReceiver.run();
    }
}
 ``` 
 
### 4、 整合Spring实现消息发送和接收，在整合之前我们需要添加jar包;

这些jar包可以在D:\apache-activemq-5.8.0\lib这个lib目录中找到，添加完jar包后就开始编码工作。
消息发送者

``` java
package com.hoo.mq.spring.support;
 
import java.util.Date;
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.Session;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.FileSystemXmlApplicationContext;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.jms.core.MessageCreator;
 
/**
 * <b>function:</b> Spring JMSTemplate 消息发送者
 * @author hoojo
 * @createDate 2013-6-24 下午02:18:48
 * @file Sender.java
 * @package com.hoo.mq.spring.support
 * @project ActiveMQ-5.8
 * @blog http://blog.csdn.net/IBM_hoojo
 * @email hoojo_@126.com
 * @version 1.0
 */
public class Sender {
 
    public static void main(String[] args) {
        ApplicationContext ctx = new FileSystemXmlApplicationContext("classpath:applicationContext-*.xml");
        JmsTemplate jmsTemplate = (JmsTemplate) ctx.getBean("jmsTemplate");
 
        jmsTemplate.send(new MessageCreator() {
            public Message createMessage(Session session) throws JMSException {
                MapMessage message = session.createMapMessage();
                message.setString("message", "current system time: " + new Date().getTime());
                
                return message;
            }
        });
    }
}
``` 

消息接收者

``` java
package com.hoo.mq.spring.support;
 
import java.util.Map;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.FileSystemXmlApplicationContext;
import org.springframework.jms.core.JmsTemplate;
 
/**
 * <b>function:</b> Spring JMSTemplate 消息接收者
 * @author hoojo
 * @createDate 2013-6-24 下午02:22:32
 * @file Receiver.java
 * @package com.hoo.mq.spring.support
 * @project ActiveMQ-5.8
 * @blog http://blog.csdn.net/IBM_hoojo
 * @email hoojo_@126.com
 * @version 1.0
 */
public class Receiver {
 
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        ApplicationContext ctx = new FileSystemXmlApplicationContext("classpath:applicationContext-*.xml");  
          
        JmsTemplate jmsTemplate = (JmsTemplate) ctx.getBean("jmsTemplate");  
        while(true) {  
            Map<String, Object> map =  (Map<String, Object>) jmsTemplate.receiveAndConvert();  
            
            System.out.println("收到消息：" + map.get("message"));  
        }  
    }
}
``` 

这里主要是用到了JmsTemplate这个消息模板，这个对象在spring的IoC容器中管理，所以要从spring的容器上下文中获取。下面看看spring的配置文件applicationContext-beans.xml内容：

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans 
    http://www.springframework.org/schema/beans/spring-beans-3.1.xsd
    http://www.springframework.org/schema/context
    http://www.springframework.org/schema/context/spring-context-3.1.xsd">
    
    <!-- 连接池  -->
    <bean id="pooledConnectionFactory" class="org.apache.activemq.pool.PooledConnectionFactory" destroy-method="stop">  
        <property name="connectionFactory">  
            <bean class="org.apache.activemq.ActiveMQConnectionFactory">  
                <property name="brokerURL" value="tcp://localhost:61616" />  
            </bean>  
        </property>  
    </bean>  
      
    <!-- 连接工厂 -->
    <bean id="activeMQConnectionFactory" class="org.apache.activemq.ActiveMQConnectionFactory">  
        <property name="brokerURL" value="tcp://localhost:61616" />  
    </bean>  
    
    <!-- 配置消息目标 -->
    <bean id="destination" class="org.apache.activemq.command.ActiveMQQueue">  
        <!-- 目标，在ActiveMQ管理员控制台创建 http://localhost:8161/admin/queues.jsp -->
        <constructor-arg index="0" value="hoo.mq.queue" />  
    </bean>  
 
    <!-- 消息模板 -->
    <bean id="jmsTemplate" class="org.springframework.jms.core.JmsTemplate">  
        <property name="connectionFactory" ref="activeMQConnectionFactory" />  
        <property name="defaultDestination" ref="destination" />  
        <property name="messageConverter">  
            <bean class="org.springframework.jms.support.converter.SimpleMessageConverter" />
        </property>  
    </bean>  
</beans>
``` 

这里的整合就比较简单了，如果你是web工程，那你在需要用jms的时候，只需用注入jmsTemplate即可。

