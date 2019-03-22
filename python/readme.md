|知识点|说明|  
|---|---|  
|[基础](基础.MD)|数据类型与函数；数据类型包括：整数、浮点数、字符串、布尔、空值、列表（List和tuple-一旦初始化就不能修改）、字典（dict相当与其他语言的map）、set（无重复值的List）等多种数据类型，还允许创建自定义数据类型函数：1.位置参数（和java一样）2.默认参数（def power(x, n=2):）3.可变参数（def calc(*numbers)） 4.关键字参数（def person(name, age, **kw):）5.命名关键字参数（def person(name, age, *, city, job):） 6.参数组合（ def f1(a, b, c=0, *args, **kw):） |
|[进阶](进阶.MD)|切片；迭代；列表生成式（生成list [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]可以用list(range(1, 11))） ；生成器；函数式编程；返回函数；匿名函数；装饰器；偏函数；模块；作用域|
|[面向对象.MD](面向对象.MD)| 继承和多态；实例属性和类属性；MixIn（多重继承）；枚举类；定制类；元类；|
|[线程.MD](线程.MD)|进程；Pool；进程间通信；多线程；Lock（Python解释器由于设计时有GIL全局锁，导致了多线程无法利用多核。多线程的并发在Python中就是一个美丽的梦。）；ThreadLocal;分布式进程 |
|[模块.MD](模块.MD)|常用模块说明：1.datetime，collections（namedtuple，deque（deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈），OrderedDict（使用dict时，Key是无序的。OrderedDict的Key会按照插入的顺序排列），Counter（Counter是一个简单的计数器，例如，统计字符出现的个数）） ，base64，hashlib（提供了常见的摘要算法，如 ，SHA1等等），itertools提供了非常有用的用于操作迭代对象的函数等等|
|[网络编程.MD](网络编程.MD)|TCP\IP;UDP;邮件 |
|[io.MD](io.MD)| 文件的读写包括二进制文件的读写；StringIO和BytesIO；操作文件和目录；pickle模块来实现序列化；异步IO|
|[数据库.MD](数据库.MD)|MySQL |
|[web.MD](web.MD)|WSGI;Flask DEMO;其他web框架简介 |
