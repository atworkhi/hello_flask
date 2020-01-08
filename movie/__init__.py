import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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
    from movie.models import User
    user = User.query.get(int(user_id))
    return user

# 模板上下文处理函数
@app.context_processor
def inject_user():
    from movie.models import User
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}


from movie import views, errors, commands
