#!/usr/bin/env python3
# coding=utf-8

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            row_text,
            [row.text for row in rows]
        )

    def test_layout_and_styling(self):
        # 小张访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 他看到输入框完美的居中显示
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # 他新建了一个清单，看到输入框仍完美的居中显示
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 小张听说有一个很酷的在线待办事项应用
        # 他去看了这个应用的首页
        self.browser.get(self.live_server_url)

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

        # 他按回车键后, 被带到了一个新URL
        # 这个页面的待办事项表格中显示了“1: 买苹果笔记本”
        inputbox.send_keys(Keys.ENTER)
        xiaozhang_list_url = self.browser.current_url
        self.assertRegex(xiaozhang_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: 买苹果笔记本')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了“用苹果笔记本打魔兽世界”
        # 小张做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('用苹果笔记本打魔兽世界')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，他的清单中显示了这两个待办事项
        self.check_for_row_in_list_table('1: 买苹果笔记本')
        self.check_for_row_in_list_table('2: 用苹果笔记本打魔兽世界')

        # 现在一个叫做小李的新用户访问了网站

        # 我们使用一个新浏览器会话
        # 确保小张的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 小李访问首页
        # 页面中看不到小张的待办事项清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买苹果笔记本', page_text)
        self.assertNotIn('用苹果笔记本打魔兽世界', page_text)

        # 小李输入一个新的待办事项，新建一个清单
        # 他不像小张那样有兴致
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('买营养快线')
        inputbox.send_keys(Keys.ENTER)

        # 小李获得了他的唯一URL
        xiaoli_list_url = self.browser.current_url
        self.assertRegex(xiaoli_list_url, '/lists/.+')
        self.assertNotEqual(xiaoli_list_url, xiaozhang_list_url)

        # 这个页面中还是没有小张的待办事项清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买苹果笔记本', page_text)
        self.assertIn('买营养快线', page_text)
