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














