from flask import render_template
from movie import app

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
