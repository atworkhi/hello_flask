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







