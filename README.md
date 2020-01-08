# Flask Hello
学习出处：http://helloflask.com/tutorial/
## Hello-01
代码: `git checkout v0.1`
### 环境变量
- FLASK_APP  
将文件名命名"app.py",flask默认会假设程序存储在app/wsgi文件中，所以可以直接运行 flask run  
如果命名其他文件名，则需要设置"FLASK_APP"环境变量
- FLASK_ENV  
设置程序运行的环境，默认为"production".  
实际开发环境中，需要将其开启为调试模式即可，调试模式环境变量"development"

### 设置调试模式
> pip install python-dotenv  

为了避免每次打开终端都需要设置环境变量，安装上面的包管理系统环境变量  
python-dotenv会根据项目根目录".flaskenv"和".env"文件读取环境变量并设置：  
- .flaskenv: 存储flask命令行系统相关的公开环境变量
- .env：用来存储敏感数据(不要提交的git仓库)

在".flaskenv"添加如下内容，可以开启调试模式
> FLASK_ENV=development  

### URL 规则
  1. 使用路由以"/"结尾，访问url时候添加末尾"/"都能访问(200, 302)，如果不以"/"结尾，则访问url时添加末尾"/"，则不能进行正确访问
  2. 一个视图函数可以绑定多个url，通过附加多个装饰器实现
   ```
@app.route('/')
@app.route('/index')
def hello():
    return "hello flask runing...."
   ```
  3. 路由参数传递，在路由后增加参数使用"<param>"
```
@app.route('/user/<name>')
def username(name):
    return "hello you are: %s" %name
```
   4. 视图函数名：视图函数名是自定义的，代表某个路由的端点(endpoint),同时用来生成url,对于程序的url，为了避免手写，flask提供了"url_for"函数生成url，它接受的第一个参数是端点值，默认为视图函数名称
## 模板和静态文件
按照默认设置，flask会在应用程序的根目录的"templates"目录中寻找模板，在同级目录的"static"目录中寻找静态资源文件
### 模板
代码: `git checkout v0.2`  
- {{  }} :插值
- {% %}:标记语句(if for等) 注意{% endxx %}
- {#  #}: 注释
- {% extend 'xxx' %}: 继承
- {% macro xxx %}: 宏
- {% include 'xxx' %}: 包含
- {{ 变量|过滤器 }}

编写主页模板templates/index.html
编写app.py并在里面初始化数据：
修改路由进行模板渲染
```
@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)
```

### 静态资源
代码: `git checkout v0.3`   
在html中引入静态资源所在的url需要使用`url_for()`函数(第一章有此函数的用法),在静态资源文件中需要传入的端点值为"static",同时使用filename参数传入相对于static文件名  
`<img src="{{ url_for('static', filename='foo.jpg') }}"`

- 添加Favicon:修改index.html的head
```
<link rel="icon" href="{{ url_for('static', filename='favico.png') }}">
```
- 添加其他图片  
创建"static"其中添加两张图片并修改html引用他们
```
<head>
    ...
    <img src="{{ url_for('static', filename='images/avatar.png') }}" alt="Avatar">
    <title>{{ name }}'s Info</title>
    ...
    <img alt="Walking..." src="{{ url_for('static', filename='images/totoro.gif') }}"
</body>
```
- 添加CSS
在static下创建style.css,在html的head标签页中引入 并在相关属性下添加对应class

`<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" `  
- 更多的样式可是使用Bootstrap-flask:  
 https://bootstrap-flask.readthedocs.io/en/latest/
  
## 数据库
代码: `git checkout v0.4`   
使用 SQLAlchemy操作数据库，Flask提供了简化的第三方库的继承，集成的SQLAlchemy的插件叫：Flask-SQLAlchemy
> pip install flask-sqlalchemy

### 初始化
- 初始化  
```
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app=app)  # 初始化数据库
```
- 连接数据库
为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要设置和定义一些配置变量。Flask 提供了一个统一的接口来写入和获取这些配置变量： Flask.config 字典。配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前
`SQLALCHEMY_DATABASE_URI`变量来告诉 SQLAlchemy 数据库连接地址
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')  # 连接数据库
# 注意 使用win使用"///"不是四个
import os, sys
WIN = sys.platform.startswith('win')  # 判断系统
if WIN:  # windows 使用三斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')  # 连接数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
db = SQLAlchemy(app=app)
```
- 创建数据模型  
模型类要声明继承 db.Model  
每一个属性都I要实例化db.Column (见代码示例)   
如果需要指定表明使用"__tablename__"属性

| 常用字段 |  说明 |
|----|----|
| db.Integer | 整型|
| db.String(size) | 字符串 |
| db.Text | 长文本 |
| db.DateTime | 时间日期(Python datetime对象)
| db.Float | 浮点数 |
| db.Boolean | 布尔值 |

- 创建数据库表
> $ flask shell   
> from app import db  
> db.create_all()  # 创建表  
> db.drop_all()  # 删除表  

每次创建表和数据库改变需要删除表，这样也损坏了数据，如果不想破坏数据库的数据，可以使用数据库迁移工具(集成了Alembic的flask-migrate)  
创建数据库需要进入到flask shell中,因此可以写个自定义命令操作数据库
```
import click
# 将初始化数据 注册为命令 flask initdb
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.') # 设置选项
def initdb(drop):
    '''
    Init the database.
    '''
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('initialized database.') # 输出提示信息
# flask initdb 创建数据表
# flask initdb --drop # 删除表后重建
```
### CRUD
- 增加
```
>>> from app import User, Movie # 导入模型类
>>> user = User(name='Grey Li') # 创建一个 User 记录
>>> m1 = Movie(title='Leon', year='1994') # 创建一个 Movie 记
>>> m2 = Movie(title='Mahjong', year='1996') # 再创建一个 Movi记录
>>> db.session.add(user) # 把新创建的记录添加到数据库会话
>>> db.session.add(m1)>>> db.session.add(m2)
>>> db.session.commit() # 提交数据库会话，只需要在最后调用一次即
```
- 查询
> <模型类>.query.<过滤方法>.<查询方法>

**过滤方法：**

| 过滤方法 |说明 |
|---|---|
| filter() | 使用指定的规则过滤记录，返回新产生的查询对象 |
| filter_by() | 使用指定规则过滤记录（以关键字表达式的形式），返回新产生的查询对象|
| order_by() | 根据指定条件对记录进行排序，返回新产生的查询对象 |
| group_by() | 根据指定条件对记录进行分组，返回新产生的查询对象 |

**查询方法：**

| 查询方法 | 说明 |
|---|---|
| all() | 返回包含所有查询记录的列表 |
| first() | 返回查询的第一条记录，如果未找到，则返回None |
| get(id) | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回None |
| count() | 返回查询结果的数量 |
| first_or_404() | 返回查询的第一条记录，如果未找到，则返回404错误响应 |
| get_or_404(id) | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回404错误响应 | 
| paginate() | 返回一个Pagination对象，可以对记录进行分页处理 |
```
>>> from app import Movie # 导入模型类
>>> movie = Movie.query.first() # 获取 Movie 模型的第一个记录（返回模型类实例）
>>> movie.title # 对返回的模型类实例调用属性即可获取记录的各字段数据
'Leon'
>>> movie.year
'1994'
>>> Movie.query.all() # 获取 Movie 模型的所有记录，返回包含多个模型类实例的列表
[<Movie 1>, <Movie 2>]
>>> Movie.query.count() # 获取Movie 模型所有记录的数量
2
>>> Movie.query.get(1) # 获取主键值为 1 的记录
<Movie 1>
>>> Movie.query.filter_by(title='Mahjong').first() # 获取title字段值为 Mahjong 的记录
<Movie 2>
>>> Movie.query.filter(Movie.title=='Mahjong').first() # 等同于上面的查询，但使用不同的过滤方法
<Movie 2>
```
- 修改
```
>>> movie = Movie.query.get(2)
>>> movie.title = 'WALL-E' # 直接对实例属性赋予新的值即可
>>> movie.year = '2008
>>> db.session.commit() # 注意仍然需要调用这一行来提交改动
```
- 删除
```
>>> movie = Movie.query.get(1)
>>> db.session.delete(movie) # 使用db.session.delete() 方法删除记录，传入模型实例
>>> db.session.commit() # 提交改动
```
### app.py操作数据库
修改index()使其读取数据库数据并修改对应模板`{{ user.name }}`  
创建命令`flask forge` 生成数据到数据库
```
# 生成数据到数据库
@app.cli.command()
def forge():
    '''Generate fake data.'''
    db.create_all()
    name = 'Han Star'

    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo("Done....")
```

## 模板优化
代码: `git checkout v0.5`   
- 创建404页面  
  添加：templates/404.html并添加app中的404路由
```
@app.errorhandler(404)  # 传入错误代码
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html', user=user), 404 # 返回模板和状态码
```
- 使用模板上下文处理函数  
因为许多模板都需要使用变量，可使用`app.context_processor`装饰器注册模板上下文处理函数，这个函数返回变量会注入到每个模板环境中，可以在每个模板环境中使用
```
@app.context_processor
def inject_user():  # 可以随意起名
    user = User.query.first() 
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}
```
接下来可以删除404和主页的user变量和模板关键字

- 使用模板继承  
创建base.html作为基模板，将html中通用的部分提取出来,并添加新样式  
模板继承重构index.html和404html(以前的html备份为.bak)
- 添加IMDb连接  
在主页模板中，为每条资源添加一个IMDb连接，这个连接的href属性我为IMDb搜索页面的url,关键词为电影标题,并添加样式
```
<span class="float-right">
            <a class="imdb" href="https://www.imdb.com/find?q={{ movie.title }}" target="_blank"
                title="Find this movie on IMDb">IMDb</a>
        </span>
```
- 添加400和500的处理页面并把错误页面统一移动到errors目录
- 如果电影标题为中文恶意使用豆瓣:`https://movie.douban.com/subject_search?
search_text={{ movie.title }}`

## 表单操作
代码: `git checkout v0.6`   
实际对数据的增删改查

### 增加
- 创建表单
在首页中添加一个表单,并设置"autocomplete"属性off关闭自动完成，还添加了"required",如果用户没输入就提交了，则会显示错误,并创建表单对应的css  
- 提交数据 修改index()函数使其支持POST并提交添加数据
```
from flask import request, url_for, redirect, flash
# request 请求路径(request.path)
# request 请求方法(request.method)
# request 请求表单(request.form)
# request 字符串(request.args)
```
- flash 消息  
使用直接`flash(message)` ,在内部会吧消息存储到Flask提供的session对象中，session用来在请求之间存储数据，它会把数据签名后存储到浏览器Cookie中，所以要设置签名密钥:
> app.config['SECRET_KEY'] = 'dev' # 等同于 app.secret_key = 'dev' 
 
在基模板中(base.html)中使用`get_flashed_messages()`获取提示消息并显示,并为其增加alert样式
```
<!-- 插入到页面标题上方 -->
{% for message in get_flashed_messages() %}
<div class="alert">{{ message }}</div>
{% endfor %}
<h2>...</h2>
```
还需要再服务器增加验证`if not ....`,实际开发中用第三方框架WTForms(https://github.com/wtforms/wtforms)实现验证和表单
- 重定向使用`redirect()`

### 修改
在app.py中添加修改需要视图函数"edit"
```python
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.') 
        return redirect(url_for('index'))  # 重定向首页
    return render_template('edit.html', movie=movie)
```
添加 edit.html 并修改 index.html增加edit超链接
```
<a href="{{ url_for('edit', movie_id=movie.id) }}">Edit</a>
```
### 删除
修改app.py 增加删除的视图函数"delete"
```
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))
```
在首页(index.html)添加删除链接
```
<form class="inline-form" method="post" action="{{ url_for('delete', movie_id=movie.id) }}">
                <input class='btn' type="submit" name="delete" value="delete" onclick="return confirm('Are you sure?')">
            </form>
```
为了让表单中的删除按钮和编辑拍成一行，添加css定义
```
.inline-form {
    display: inline;
}
```
## 用户认证
代码: `git checkout v0.7`  
### 安全密码
flask依赖"Werkzeug"内置了用于生成和验证密码散列值函数
- werkzeug.security.generate_password_hash() 生成密码散列
- werkzeug.security.check_password_hash() 效验散列密码
```
>>> from werkzeug.security import generate_password_hash, check_password_hash
>>> pw_hash = generate_password_hash('dog') # 为密码 dog 生成密码散列值
>>> pw_hash # 查看密码散列值
'pbkdf2:sha256:50000$mm9UPTRI$ee68ebc71434a4405a28d34ae3f170757fb424663dc0ca15198cb881edc0978f'
>>> check_password_hash(pw_hash, 'dog') # 检查散列值是否对应密码 dog
True
>>> check_password_hash(pw_hash, 'cat') # 检查散列值是否对应密码 cat
False
```
在user模型中增加username字段和pasoword_hash字段，并实现设置和验证密码(代码在app的user类中),有序修改了表结构，需要重新生成数据库
> flask initdb --drop
### 生成admin
此程序就不设计注册页面，可以编写一个命令，创建管理员的函数"admin()"
```
运行生成：
$ flask admin
Username: hanguoxing
Password:
Repeat for confirmation:
Creating user...
Admin Create over!!!
```
### 使用`Flask-Login`实现认证
安装：
> pip install flask-login

初始化Flask-login,除了实例化扩展外，还需要实现一个"用户加载回调函数",它还提供了`current_user`变量，注册这个函数的目的是当程序运行后，如果用户已经登录，`current_user`变量的值会是当前用户的用户模型类记录。另一个步骤是让存储用户的User模型类继承Flask-login提供和`UserMixin`类，这样会让user类拥有几个用于判断认证状态的属性和方法(`is_authenticated`如果当前用户登录返回True,否则返回false)
```python
from flask_login import LoginManager, UserMixin
login_manage = LoginManager(app)  # 实例化拓展
@login_manage.user_loader
def load_user(user_id):
    '''创建用户加载回调函数，接收用户ID作为参数'''
    user = User.query.get(int(user_id))
    return user
# 创建数据模型
class User(db.Model, UserMixin):
    ...
```

- 登录  
使用`login_user()`函数实现登录，需要传入用户模型类对象作为参数。如app中的login函数, 并创建对应的模板login.html
> from flask_login import login_user

- 登出  
和登录相对，登出操作需要调用`logout_user`函数,添加logout函数
> from flask_login import logout_user

- 认证保护
> from flask_login import login_required

认证保护就是页面上不登陆禁止访问的资源，比如登出 增加 编辑 删除等页面，添加认证保护只需要在函数上增加`@login_required`注解即可，如果未登录访问敏感资源，会重定向到登录页面，为了实现重定向，还需要设置`login_manager.login_view='login'`

其中注意由于新增的和首页在一个函数内，使其即处理get又处理post,我们仅使未登录的用户不能新增，因此不能使用注解限制，而要在post请求内部进行过滤
```
from flask_login import current_user
if not current_user.is_authenticated:  # 未认证
    return redirect(url_for('index'))
```

- 添加修改用户名  
在app中增加"settings"函数，并实现对应的模板

- 在index页面中增加登录保护,使用"if current_user.is_authenticated",在模板渲染时会首先判断是否为真，如果未登录为False,则此部分不会被渲染  
修改index的增加表单和修改删除按钮，修改base的导航增加登录登出修改用户名
```
{% if current_user.is_authenticated %}
<form method="post">
    Name <input type="text" name="title" autocomplete="off" requ ired>
    Year <input type="text" name="year" autocomplete="off" requi red>
    <input class="btn" type="submit" name="submit" value="Add">
</form>
{% endif %}
...
{% if current_user.is_authenticated %}
<form class="inline-form" method="post" action="{{ url_for('delete', movie_id=movie.id) }}">
<input class='btn' type="submit" name="delete" value="delete" onclick="return confirm('Are you sure?')">
</form>
<a class="btn" href="{{ url_for('edit', movie_id=movie.id) }}">Edit</a>
{% endif %}

<!--base.html-->
{% if current_user.is_authenticated %}
<li><a href="{{ url_for('settings') }}">Settings</a></li>
<li><a href="{{ url_for('logout') }}">Logout</a></li>
{% else %}
<li><a href="{{ url_for('login') }}">Login</a></li>
{% endif %}
```

## 测试
代码: `git checkout v0.8`    
在未添加测试的时候，每次添加新功能都需要手动在浏览器中进行访问，如果在功能复杂程序中，每次修改或添加新功能，都手动测试所有功能，会产生很大的工作量，另一方面，手动运行测试也并不可靠，因此，我们需要编写自动化测试

### 单元测试
单元测试是对程序中的函数等独立单元编写的测试，它是自动化测试最重要的形式，Python标准库中的测试框架`unittest`来编写单元测试  
如： 测试如下函数study.py:
```python
def hello(to=None):
    if to:
        return 'Hello, %s' % to
    return 'Hello!'
```
编写单元测试test_study.py,并运行此测试文件：
```
import unittest
from study import hello


class HelloTestCase(unittest.TestCase):  # 测试用例
    def setUp(self):  # 测试固件
        pass

    def tearDown(self):  # 测试固件
        pass

    def test_hello(self):  # 第一个测试
        rv = hello()
        self.assertEqual(rv, 'Hello!')

    def test_hello_to_somebody(self):  # 第二个测试
        rv = hello(to='hi')
        self.assertEqual(rv, 'Hello, hi!')

if __name__ == "__main__":
    unittest.main()
```
**说明：**  
测试用例继承`unittest.TestCase`类，在这个类中创建以`test_`开头的方法将会被视为测试方法。内容为空的两个方法时特殊方法，因为是测试固件的，用来执行一些特殊操作,"setUp"方法会在每个测试方法执行前调用，"tearDown"方法会在每个测试方法执行后调用  
每一个测试方法(test_xxx)对应一个要测试的函数/功能/使用场景，在测试方法中使用断言方法来判断程序功能是否正常，常用的断言如下：
1. assertEqual(a,b)
2. assertNotEqual(a,b)
3. assertTrue(x)
4. assertFalse(x)
5. assertIs(a,b)
6. assertIsNot(a,b)
7. assertIsNone(x)
8. assertIsNotNone(x)
9. assertIn(a,b)
10. assertNotIn(a,b)

### 测试Flask程序
创建一个test_flask.py脚本来存储测试代码:
- 测试固件
```
import unittest
from app import app, db, Movie, User

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # 配置更新
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        # 创建数据库和表
        db.create_all()
        # 创建测试数据
        user = User(name="Test", username='test')
        user.set_password('123')
        movie = Movie(title='Test Movie', year='2020')
        # 使用add_all放管服测试添加多个实例
        db.session.add_all([user, movie])
        db.session.commit()

        self.client = app.test_client()  # 创建客户端测试
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除表

    def test_app_exist(self):
        self.assertIsNotNone(app)  # 测试程序实例是否存在

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])  # 测试程序是否处于测模式
```
说明：  
在"setUp"方法中，更新了两个配置变量`TESTING`设置为True来开启测试模式，这样在运行出错时不会输出多余信息，`SQLALCHEMY_DATABASE_URI`设置为"sqlite:///:memory:"会使用SQLite内存型数据库,不会影响开发时的数据库文件，内存数据库速度更快，并且创建了两个类属性分别为测试客户端(模拟客服端请求)和测试命令运行器(触发自定义命令)  

**测试客户端：**  
`app.test_client()`返回测试客户端对象，可以模拟浏览器。使用类属性"self.client"保存，对他调用get()方法等于发送get请求，post()方法发送POST请求,如此 编写测试404页面(test_404_page)和主页(test_index_page)  
测试数据操作相关功能，必须登录账户才能发送，因此编写一个登录的辅助方法，并添加创建、更新和删除
```
 def login(self):
        """登录辅助方法"""
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)   # 跟随重定向
```
添加测试登录保护、登录、登出、设置改名等

- 测试命令  
除了测试程序的各个视图函数，还需要测试自定义的命令:`app.test_cli_runner()`返回一个命令运行器对象，可以使用self.runner保存，通过对他调用`invoke`方法执行命令对象，或者使用`args`关键字直接给出命令参数列表，invoke返回的命令执行结果，它的output属性返回输出信息

- 添加main
```python
    if __name__ == "__main__":
        unittest.main()
```

- 运行测试,哪里有错误就修改哪里
> python test_flask.py

### 测试覆盖率
为了更完善的测试，可以使用`Coverage.py`来检测测试覆盖率
> pip install coverage  # 安装
> coverage run --source=app test_flask.py  # 测试覆盖率

由于只需要检查程序脚本app.py的测试覆盖率，所以使用"--source"选项指定要检查的模块或包
> coverage report # 查看覆盖率
> coverage html  # 获取html报告

注意：使用unittest并不是唯一选择，也可使用第三方工具`pytest:`https://pytest.org/en/latest/

## 重构项目
代码: `git checkout v0.9`  
由于所有代码都集中在app文件中，对以后的开发和维护造成困难，因此需要对代码进行重构
- 创建movie目录，作为包文件夹，并将static和templates移动到此
- __init__.py 包构造文件，创建程序实例
- views.py 视图函数
- errors.py  错误处理函数
- models.py 模型类
- commands.py 命令函数

#### __init__.py
创建程序实例，初始化拓展都可以放到此文件中.
在构造文件中，为了让视图函数、错误处理函数和命令函数注册到程序实例上，我们需要在这里导入这几个模块。但是因为这几个模块同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。同样的， load_user() 函数和 inject_user() 函数中使用的模型类也在函数内进行导入

修改test的引入并运行测试
> coverage run --source=movie test_flask.py

启动程序
> FLASK_APP=movie

## 上线
代码: `git checkout v0.9` 
应用通常两种部署(本地部署和云部署)，在此处使用云平台[PythonAnyWhere](https://www.pythonanywhere.com)

- 生成依赖表(pipenv 可以忽略)
> pip freeze > requirements.txt

- 对于有些配置需要在生产环境下使用不同的值，为了使配置更加灵活，需要在生产环境下使用的配置优先读取，如果没有读取到，则使用默认值
```
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
```
- 在部署程序时，我们不会使用Flask内置服务器，因此对于手动写到.env文件的变量，需要手动使用python-dotenv导入，见app.py
```
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    
from movie import app
```





