# Java网络IO	
### BIO、NIO、AIO适用场景分析: 	
    BIO方式适用于连接数目比较小且固定的架构，这种方式对服务器资源要求比较高，并发局限于应用中，JDK1.4以前的唯一选择，但程序直观简单易理解。             
    
    NIO方式适用于连接数目多且连接比较短（轻操作）的架构，比如聊天服务器，并发局限于应用中，编程比较复杂，JDK1.4开始支持。       
    
    AIO方式使用于连接数目多且连接比较长（重操作）的架构，比如相册服务器，充分调用OS参与并发操作，编程比较复杂，JDK7开始支持。                      
	


### NIO服务端序列图

![image](https://github.com/miozeng/Review/blob/master/MQ%E4%B8%8E%E5%90%84%E7%A7%8D%E5%8D%8F%E8%AE%AE/NIOserver.png)
步骤一：打开ServerSocketChannel，用于监听客户端的连接，它是所有客户端连接的父管道，代码示例如下：
``` java
	ServerSocketChannel acceptorSvr = ServerSocketChannel.open();
``` 
步骤二：绑定监听端口，设置连接为非阻塞模式，示例代码如下：
``` java
	acceptorSvr.socket().bind(new InetSocketAddress(InetAddress.getByName(“IP”), port));
	acceptorSvr.configureBlocking(false);
``` 
步骤三：创建Reactor线程，创建多路复用器并启动线程，代码如下：
``` java
	Selector selector = Selector.open();
	New Thread(new ReactorTask()).start();
``` 
步骤四：将ServerSocketChannel注册到Reactor线程的多路复用器Selector上，监听ACCEPT事件，代码如下：
``` java
	SelectionKey key = acceptorSvr.register( selector, SelectionKey.OP_ACCEPT, ioHandler);
``` 
步骤五：多路复用器在线程run方法的无限循环体内轮询准备就绪的Key，代码如下：
``` java
	int num = selector.select();
	Set selectedKeys = selector.selectedKeys();
	Iterator it = selectedKeys.iterator();
	while (it.hasNext()) {
	     SelectionKey key = (SelectionKey)it.next();
	     // ... deal with I/O event ...
	}
``` 
步骤六：多路复用器监听到有新的客户端接入，处理新的接入请求，完成TCP三次握手，建立物理链路，代码示例如下：
``` java
	SocketChannel channel = svrChannel.accept();
``` 
步骤七：设置客户端链路为非阻塞模式，示例代码如下：
``` java
	channel.configureBlocking(false);
	channel.socket().setReuseAddress(true);
``` 
步骤八：将新接入的客户端连接注册到Reactor线程的多路复用器上，监听读操作，用来读取客户端发送的网络消息，代码如下：
``` java
	SelectionKey key = socketChannel.register( selector, SelectionKey.OP_READ, ioHandler);
``` 
步骤九：异步读取客户端请求消息到缓冲区，示例代码如下：
``` java
	int  readNumber =  channel.read(receivedBuffer);
``` 
步骤十：对ByteBuffer进行编解码，如果有半包消息指针reset，继续读取后续的报文，将解码成功的消息封装成Task，投递到业务线程池中，进行业务逻辑编排，示例代码如下：
``` java
01	Object message = null;
02	while(buffer.hasRemain())
03	{
04	       byteBuffer.mark();
05	       Object message = decode(byteBuffer);
06	       if (message == null)
07	       {
08	          byteBuffer.reset();
09	          break;
10	       }
11	       messageList.add(message );
12	}
13	if (!byteBuffer.hasRemain())
14	byteBuffer.clear();
15	else
16	    byteBuffer.compact();
17	if (messageList != null & !messageList.isEmpty())
18	{
19	for(Object messageE : messageList)
20	   handlerTask(messageE);
21	}
``` 
步骤十一：将POJO对象encode成ByteBuffer，调用SocketChannel的异步write接口，将消息异步发送给客户端，示例代码如下：
``` java
1	socketChannel.write(buffer);
``` 
注意：如果发送区TCP缓冲区满，会导致写半包，此时，需要注册监听写操作位，循环写，直到整包消息写入TCP缓冲区，此处不赘述，后续Netty源码分析章节会详细分析Netty的处理策略。

### NIO客户端序列图

![image](https://github.com/miozeng/Review/blob/master/MQ%E4%B8%8E%E5%90%84%E7%A7%8D%E5%8D%8F%E8%AE%AE/NIOClient.png)
步骤一：打开SocketChannel，绑定客户端本地地址（可选，默认系统会随机分配一个可用的本地地址），示例代码如下：
``` java
1	SocketChannel clientChannel = SocketChannel.open();
``` 
步骤二：设置SocketChannel为非阻塞模式，同时设置客户端连接的TCP参数，示例代码如下：
``` java
1	clientChannel.configureBlocking(false);
2	socket.setReuseAddress(true);
3	socket.setReceiveBufferSize(BUFFER_SIZE);
4	socket.setSendBufferSize(BUFFER_SIZE);
``` 
步骤三：异步连接服务端，示例代码如下：
``` java
1	boolean connected = clientChannel.connect(new InetSocketAddress(“ip”,port));
``` 
步骤四：判断是否连接成功，如果连接成功，则直接注册读状态位到多路复用器中，如果当前没有连接成功（异步连接，返回false，说明客户端已经发送sync包，服务端没有返回ack包，物理链路还没有建立），示例代码如下：
``` java
1	if (connected)
2	{
3	    clientChannel.register( selector, SelectionKey.OP_READ, ioHandler);
4	}
5	else
6	{
7	    clientChannel.register( selector, SelectionKey.OP_CONNECT, ioHandler);
8	}
``` 	
步骤五：向Reactor线程的多路复用器注册OP_CONNECT状态位，监听服务端的TCP ACK应答，示例代码如下：
``` java
1	clientChannel.register( selector, SelectionKey.OP_CONNECT, ioHandler);
``` 
步骤六：创建Reactor线程，创建多路复用器并启动线程，代码如下：
``` java
1	Selector selector = Selector.open();
2	New Thread(new ReactorTask()).start();
``` 
步骤七：多路复用器在线程run方法的无限循环体内轮询准备就绪的Key，代码如下：
``` java
	int num = selector.select();
	Set selectedKeys = selector.selectedKeys();
	Iterator it = selectedKeys.iterator();
	while (it.hasNext()) {
	if (key.isConnectable())
	  //handlerConnect();
	}
``` 
步骤九：判断连接结果，如果连接成功，注册读事件到多路复用器，示例代码如下
``` java
	if (channel.finishConnect())
	  registerRead();
``` 
步骤十：注册读事件到多路复用器：
``` java
	clientChannel.register( selector, SelectionKey.OP_READ, ioHandler);
``` 
步骤十一：异步读客户端请求消息到缓冲区，示例代码如下：
``` java
	int  readNumber =  channel.read(receivedBuffer);
``` 
步骤十二：对ByteBuffer进行编解码，如果有半包消息接收缓冲区Reset，继续读取后续的报文，将解码成功的消息封装成Task，投递到业务线程池中，进行业务逻辑编排，示例代码如下：
``` java
	Object message = null;
	while(buffer.hasRemain())
	{
	       byteBuffer.mark();
	       Object message = decode(byteBuffer);
	       if (message == null)
	       {
	          byteBuffer.reset();
	          break;
	       }
	       messageList.add(message );
	}
	if (!byteBuffer.hasRemain())
	byteBuffer.clear();
	else
	    byteBuffer.compact();
	if (messageList != null & !messageList.isEmpty())
	{
	for(Object messageE : messageList)
	   handlerTask(messageE);
	}
``` 
步骤十三：将POJO对象encode成ByteBuffer，调用SocketChannel的异步write接口，将消息异步发送给客户端，示例代码如下：
``` java
1	socketChannel.write(buffer);
``` 
###  AIO
NIO2.0引入了新的异步通道的概念，并提供了异步文件通道和异步套接字通道的实现。异步通道提供两种方式获取获取操作结果：		
通过java.util.concurrent.Future类来表示异步操作的结果；		
在执行异步操作的时候传入一个java.nio.channels.		
CompletionHandler接口的实现类作为操作完成的回调。		
NIO2.0的异步套接字通道是真正的异步非阻塞IO,它对应Unix网络编程中的事件驱动IO（AIO），它不需要通过多路复用器（Selector）对注册的通道进行轮询操作即可实现异步读写，简化了NIO的编程模型。
