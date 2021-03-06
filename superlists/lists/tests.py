#!/usr/bin/env python3
# coding=utf-8

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import (Item, List)


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = '第一个待办事项'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = '第二个待办事项'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '第一个待办事项')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, '第二个待办事项')
        self.assertEqual(second_saved_item.list, list_)


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
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='待办事项1', list=correct_list)
        Item.objects.create(text='待办事项2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='其它待办事项1', list=other_list)
        Item.objects.create(text='其它待办事项2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, '待办事项1')
        self.assertContains(response, '待办事项2')
        self.assertNotContains(response, '其它待办事项1')
        self.assertNotContains(response, '其它待办事项2')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)


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

        new_list = List.objects.first()

        self.assertRedirects(
            response,
            '/lists/%d/' % (new_list.id,)
        )


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': '一个已有清单中的新待办事项'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '一个已有清单中的新待办事项')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': '一个已有清单中的新待办事项'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
