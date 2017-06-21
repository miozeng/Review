#WSGI
Python专注于生成HTML文档。因为我们不希望接触到TCP连接、HTTP原始请求和响应格式，所以，需要一个统一的接口，让我们专心用Python编写Web业务。

这个接口就是WSGI：Web Server Gateway Interface。

WSGI接口定义非常简单，它只要求Web开发者实现一个函数，就可以响应HTTP请求。我们来看一个最简单的Web版本的“Hello, web!”：

运行WSGI服务

我们先编写hello.py，实现Web应用程序的WSGI处理函数：

    # hello.py
    def application(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'<h1>Hello, web!</h1>']
    
然后，再编写一个server.py，负责启动WSGI服务器，加载application()函数：
    # server.py
    # 从wsgiref模块导入:
    from wsgiref.simple_server import make_server
    # 导入我们自己编写的application函数:
    from hello import application
    # 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
    httpd = make_server('', 8000, application)
    print('Serving HTTP on port 8000...')
    # 开始监听HTTP请求:
    httpd.serve_forever()


由于用Python开发一个Web框架十分容易，所以Python有上百个开源的Web框架。这里我们先不讨论各种Web框架的优缺点，直接选择一个比较流行的Web框架——Flask来使用。

用Flask编写Web App比WSGI接口简单（这不是废话么，要是比WSGI还复杂，用框架干嘛？），我们先用pip安装Flask：

    $ pip install flask
然后写一个app.py，处理3个URL，分别是：

GET /：首页，返回Home；

GET /signin：登录页，显示登录表单；

POST /signin：处理登录表单，显示登录结果。

注意噢，同一个URL/signin分别有GET和POST两种请求，映射到两个处理函数中。

Flask通过Python的装饰器在内部自动地把URL和函数给关联起来，所以，我们写出来的代码就像这样

    from flask import Flask, request, render_template
    
    app = Flask(__name__)
    
    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('home.html')
    
    @app.route('/signin', methods=['GET'])
    def signin_form():
        return render_template('form.html')
    
    @app.route('/signin', methods=['POST'])
    def signin():
        username = request.form['username']
        password = request.form['password']
        if username=='admin' and password=='password':
            return render_template('signin-ok.html', username=username)
        return render_template('form.html', message='Bad username or password', username=username)
    
    if __name__ == '__main__':
        app.run()

除了Flask，常见的Python Web框架还有：

Django：全能型Web框架；

web.py：一个小巧的Web框架；

Bottle：和Flask类似的Web框架；

Tornado：Facebook的开源异步Web框架

Flask通过render_template()函数来实现模板的渲染。和Web框架类似，Python的模板也有很多种。Flask默认支持的模板是jinja2，所以我们先直接安装jinja2：
   
    <html>
    <head>
      <title>Welcome, {{ username }}</title>
    </head>
    <body>
      <p>Welcome, {{ username }}!</p>
    </body>
    </html>
除了Jinja2，常见的模板还有：

Mako：用<% ... %>和${xxx}的一个模板；

Cheetah：也是用<% ... %>和${xxx}的一个模板；

Django：Django是一站式框架，内置一个用{% ... %}和{{ xxx }}的模板。