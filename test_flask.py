import unittest

from app import app, db, Movie, User, forge, initdb


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

    def login(self):
        """登录辅助方法"""
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)   # 跟随重定向

    def test_app_exist(self):
        self.assertIsNotNone(app)  # 测试程序实例是否存在

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])  # 测试程序是否处于测模式

    def test_404_page(self):
        """test 404"""
        response = self.client.get('/nothing')  # 传入url
        data = response.get_data(as_text=True)
        self.assertIn('Page Not Found', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)  # 状态码

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Test\'s web info', data)
        self.assertIn('Test Movie', data)
        self.assertEqual(response.status_code, 200)

    def test_login_protect(self):
        """测试登录保护"""
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)

    def test_login(self):
        """测试登录"""
        response = self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Loging success.', data)
        self.assertIn('Logout', data)
        self.assertIn('Settings', data)
        self.assertIn('delete', data)
        self.assertIn('Edit', data)
        self.assertIn('<form method="post">', data)

        response = self.client.post('/login', data=dict(
            username='test',
            password='456'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        response = self.client.post('/login', data=dict(
            username='wrong',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        response = self.client.post('/login', data=dict(
            username='',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input.', data)

        response = self.client.post('/login', data=dict(
            username='test',
            password=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid input.', data)

    def test_logout(self):
        """测试登出"""
        self.login()

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('GoodBye.', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('<form method="post">', data)

    def test_settings(self):
        """测试改名"""
        self.login()

        response = self.client.get('/settings')
        data = response.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Your Name', data)

        response = self.client.post('/settings', data=dict(
            name='',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Settings updated.', data)
        self.assertIn('Invalid name.', data)

        response = self.client.post('/settings', data=dict(
            name='hanxx',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Settings update.', data)
        self.assertIn('hanxx', data)

    def test_create_item(self):
        """增加"""
        self.login()
        # 测试创建条目操作
        response = self.client.post('/', data=dict(
            title='New Movie',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item create.', data)
        self.assertIn('New Movie', data)
        # 测试创建条目操作，但电影标题为空
        response = self.client.post('/', data=dict(
            title='',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)
        # 测试创建条目操作，但电影年份为空
        response = self.client.post('/', data=dict(
            title='New Movie',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid input.', data)

    def test_update_item(self):
        """更新"""
        self.login()
        # 测试更新页面
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Edit Item', data)
        self.assertIn('Test Movie', data)
        self.assertIn('2020', data)
        # 测试更新条目操作
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie Edited',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item updated.', data)
        self.assertIn('New Movie Edited', data)
        # 测试更新条目操作，但电影标题为空
        response = self.client.post('/movie/edit/1', data=dict(
            title='',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertIn('Invalid input.', data)
        # 测试更新条目操作，但电影年份为空
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie Edited Again',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertNotIn('New Movie Edited Again', data)
        self.assertIn('Invalid input.', data)

    def test_delete_item(self):
        """测试删除"""
        self.login()
        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted.', data)
        self.assertNotIn('Test Movie', data)

    # 以下测试命令相关

    def test_forge_command(self):
        """测试生成虚拟数据"""
        result = self.runner.invoke(forge)
        self.assertIn('Done....', result.output)
        self.assertNotEqual(Movie.query.count(), 0)

    def test_initdb_command(self):
        """测试初始化数据库"""
        result = self.runner.invoke(initdb)
        self.assertIn('initialized database.', result.output)

    def test_admin_command(self):
        """测试生成管理员"""
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(args=['admin', '--username', 'hanguoxing', '--password', '123'])
        self.assertIn('Creating user...', result.output)
        self.assertIn('Admin Create over!!!', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'hanguoxing')
        self.assertTrue(User.query.first().validate_password('123'))

    def test_admin_command_update(self):
        """测试更新管理员命令"""
        result = self.runner.invoke(args=['admin', '--username', 'han', '--password', '456'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Admin Create over!!!', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'han')
        self.assertTrue(User.query.first().validate_password('456'))


if __name__ == "__main__":
    """运行测试"""
    unittest.main()
