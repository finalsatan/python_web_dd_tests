#!/usr/bin/env python3
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 小张听说有一个很酷的在线待办事项应用
        # 他去看了这个应用的首页
        self.browser.get('http://localhost:8000')

        # 他注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请他输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 他在一个文本框中输入了“买苹果笔记本”
        # 小张的爱好是使用苹果笔记本打游戏
        inputbox.send_keys('买苹果笔记本')

        # 他按回车键后，页面更新了
        # 待办事项表格中显示了“1: 买苹果笔记本”
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: 买苹果笔记本' for row in rows)
        )
        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了“用苹果笔记本打魔兽世界”
        # 小张做事很有条理
        self.fail('Finish the test!')

        # 页面再次更新，他的清单中显示了这两个待办事项

        # 小张想知道这个网站是否会记住他的清单

        # 他看到网站为他生成了了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 他访问那个URL，发现他的待办事项列表还在

        # 他很满意，去睡觉了


if __name__ == '__main__':
    unittest.main()
