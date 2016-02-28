#!/usr/bin/env python3
# coding=utf-8

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '第一个待办事项'
        first_item.save()

        second_item = Item()
        second_item.text = '第二个待办事项'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '第一个待办事项')
        self.assertEqual(second_saved_item.text, '第二个待办事项')


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        excepted_html = render_to_string(
            'home.html',
            request=request
        )
        self.assertEqual(response.content.decode(), excepted_html)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_users_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='待办事项1')
        Item.objects.create(text='待办事项2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, '待办事项1')
        self.assertContains(response, '待办事项2')


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': '一个新的待办事项'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '一个新的待办事项')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': '一个新的待办事项'}
        )

        self.assertRedirects(
            response,
            '/lists/the-only-list-in-the-world/'
        )
