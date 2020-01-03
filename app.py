from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def hello():
    return "hello flask runing...."

@app.route('/user/<name>')
def username(name):
    return "hello you are: %s" %name

@app.route('/test')
def test_url_for():
    print(url_for('hello')) # /
    print(url_for('username', name='hanguoxing')) # /user/hanguoxing
    print(url_for('test_url_for')) # /test
    print(url_for('test_url_for', page=2)) # /test?page=2
    return 'Test flask url_for'