# 测试 study 中的函数

import unittest

from study import hello


class HelloTestCase(unittest.TestCase):  # 测试用例
    def setUp(self):  # 测试固件
        pass

    def tearDown(self):  # 测试固件
        pass

    def test_hello(self):  # 第一个测试
        rv = hello()
        self.assertEqual(rv, 'Hello!')

    def test_hello_to_somebody(self):  # 第二个测试
        rv = hello(to='hi')
        self.assertEqual(rv, 'Hello, hi!')


if __name__ == "__main__":
    unittest.main()
