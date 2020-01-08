from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from movie import db


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