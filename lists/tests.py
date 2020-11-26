from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.models import Item, List
from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # Arrange
        # Act
        response = self.client.get('/')
        # Assert
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get( '/')
        self.assertEqual(Item.objects.count(), 0)


class ListAndItemModelTests(TestCase):
    def test_saving_and_retrieving_items(self):
        test_list = List()
        test_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = test_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = test_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, test_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, test_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, test_list)

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/one-list-to-rule-them-all')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        test_list = List.objects.create()
        Item.objects.create(text='Item1', list=test_list)
        Item.objects.create(text='Item42', list=test_list)

        response = self.client.get('/lists/one-list-to-rule-them-all')

        self.assertContains(response, 'Item1')
        self.assertContains(response, 'Item42')

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new',data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new',data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/one-list-to-rule-them-all')
