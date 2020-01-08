from movie import app, db
from flask import request, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from movie.models import User, Movie


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
