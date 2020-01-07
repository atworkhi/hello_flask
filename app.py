from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click
from flask import request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_login import login_user
from flask_login import logout_user, login_required
from flask_login import current_user

WIN = sys.platform.startswith('win')  # 判断系统

if WIN:  # windows 使用三斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')  # 连接数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

app.config['SECRET_KEY'] = '910416'

db = SQLAlchemy(app)  # 初始化数据库


# 始化flak-login


login_manage = LoginManager(app)  # 实例化拓展

login_manage.login_view = 'login'  # 登录


@login_manage.user_loader
def load_user(user_id):
    '''创建用户加载回调函数，接收用户ID作为参数'''
    user = User.query.get(int(user_id))
    return user


# 创建数据模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        """效验密码"""
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# 将初始化数据 注册为命令 flask initdb
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    '''
    Init the database.
    '''
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('initialized database.')  # 输出提示信息

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

# 创建管理员
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login...')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
help='The password used to login.')
def admin(username, password):
    '''创建管理员账户'''
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Admin Create over!!!')


# 模板上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = User.query.first()
        # 验证
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登录
            flash('Loging success.')
            return redirect(url_for('index'))
        flash('Invalid username or password.')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required  # 登录视图保护
def logout():
    """登出"""
    logout_user()  # 登出
    flash('GoodBye.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid name.')
            return redirect(url_for('settings'))
        current_user.name = name
        # current_user 返回当前登录用户的数据库记录对象
        # 等同以下方法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings update.')
        return redirect(url_for('index'))
    return render_template('settings.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    """首页 增加"""
    if request.method == 'POST':
        # post请求 获取表单
        if not current_user.is_authenticated:  # 未认证
            return redirect(url_for('login'))
        title = request.form.get('title')  # name值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input..')  # 显示错误消息
            return redirect(url_for('index'))  # 重定向事业
        # 保存数据表
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item create.')  # 显示创建成功
        return redirect(url_for('index'))

    movies = Movie.query.all()  # 从数据库获取电影
    return render_template('index.html', movies=movies)  # 使用上下文模板函数


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 添加登录保护
def edit(movie_id):
    """修改"""
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


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required  # 添加登录保护
def delete(movie_id):
    """删除"""
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

# 404
@app.errorhandler(404)  # 传入错误代码
def page_not_found(e):
    # user = User.query.first()
    # return render_template('404.html', user=user), 404  # 返回模板和状态码
    return render_template('errors/404.html'), 404  # 使用上下文模板函数传入user 
# 400
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400
# 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500