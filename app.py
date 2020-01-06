from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

WIN = sys.platform.startswith('win')  # 判断系统

if WIN:  # windows 使用三斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')  # 连接数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)  # 初始化数据库

# 创建数据模型


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


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


# 模板上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}
@app.route('/')
def index():
    # user = User.query.first()  # 获取用户记录
    movies = Movie.query.all()  # 从数据库获取电影
    # return render_template('index.html', user=user, movies=movies)
    return render_template('index.html', movies=movies)  # 使用上下文模板函数
# 404
@app.errorhandler(404)  # 传入错误代码
def page_not_found(e):
    # user = User.query.first()
    # return render_template('404.html', user=user), 404  # 返回模板和状态码
    return render_template('errors/404.html'), 404  # 使用上下文模板函数传入user 
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500