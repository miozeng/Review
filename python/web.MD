#WSGI
Pythonרע������HTML�ĵ�����Ϊ���ǲ�ϣ���Ӵ���TCP���ӡ�HTTPԭʼ�������Ӧ��ʽ�����ԣ���Ҫһ��ͳһ�Ľӿڣ�������ר����Python��дWebҵ��

����ӿھ���WSGI��Web Server Gateway Interface��

WSGI�ӿڶ���ǳ��򵥣���ֻҪ��Web������ʵ��һ���������Ϳ�����ӦHTTP������������һ����򵥵�Web�汾�ġ�Hello, web!����

����WSGI����

�����ȱ�дhello.py��ʵ��WebӦ�ó����WSGI����������

    # hello.py
    def application(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'<h1>Hello, web!</h1>']
    
Ȼ���ٱ�дһ��server.py����������WSGI������������application()������
    # server.py
    # ��wsgirefģ�鵼��:
    from wsgiref.simple_server import make_server
    # ���������Լ���д��application����:
    from hello import application
    # ����һ����������IP��ַΪ�գ��˿���8000������������application:
    httpd = make_server('', 8000, application)
    print('Serving HTTP on port 8000...')
    # ��ʼ����HTTP����:
    httpd.serve_forever()


������Python����һ��Web���ʮ�����ף�����Python���ϰٸ���Դ��Web��ܡ����������Ȳ����۸���Web��ܵ���ȱ�㣬ֱ��ѡ��һ���Ƚ����е�Web��ܡ���Flask��ʹ�á�

��Flask��дWeb App��WSGI�ӿڼ򵥣��ⲻ�Ƿϻ�ô��Ҫ�Ǳ�WSGI�����ӣ��ÿ�ܸ��������������pip��װFlask��

    $ pip install flask
Ȼ��дһ��app.py������3��URL���ֱ��ǣ�

GET /����ҳ������Home��

GET /signin����¼ҳ����ʾ��¼������

POST /signin��������¼��������ʾ��¼�����

ע���ޣ�ͬһ��URL/signin�ֱ���GET��POST��������ӳ�䵽�������������С�

Flaskͨ��Python��װ�������ڲ��Զ��ذ�URL�ͺ������������������ԣ�����д�����Ĵ����������

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

����Flask��������Python Web��ܻ��У�

Django��ȫ����Web��ܣ�

web.py��һ��С�ɵ�Web��ܣ�

Bottle����Flask���Ƶ�Web��ܣ�

Tornado��Facebook�Ŀ�Դ�첽Web���

Flaskͨ��render_template()������ʵ��ģ�����Ⱦ����Web������ƣ�Python��ģ��Ҳ�кܶ��֡�FlaskĬ��֧�ֵ�ģ����jinja2������������ֱ�Ӱ�װjinja2��
   
    <html>
    <head>
      <title>Welcome, {{ username }}</title>
    </head>
    <body>
      <p>Welcome, {{ username }}!</p>
    </body>
    </html>
����Jinja2��������ģ�廹�У�

Mako����<% ... %>��${xxx}��һ��ģ�壻

Cheetah��Ҳ����<% ... %>��${xxx}��һ��ģ�壻

Django��Django��һվʽ��ܣ�����һ����{% ... %}��{{ xxx }}��ģ�塣