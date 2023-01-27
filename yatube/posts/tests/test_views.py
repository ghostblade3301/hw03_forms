from django.test import TestCase, Client
from django import forms
from django.urls import reverse
from posts.models import User, Group, Post


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # create non-authorized client
        cls.guest_client = Client()
        
        # create authorized client
        cls.user1 = User.objects.create(username='Test1')
        cls.user2 = User.objects.create(username='Test2')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user1)
        cls.authorized_client.force_login(cls.user2)
        
        # create group1 in DB
        cls.group1 = Group.objects.create(
            title='Группа 1',
            slug='test-slug',
            description='Описание группы 1'
        )
        # create group2 in DB        
        cls.group2 = Group.objects.create(
            title='Группа 2',
            slug='test-slug',
            description='Описание группы 2'
        )
        
        # create test posts in group 1
        for post in range(10):
            cls.post = Post.objects.create(
                text='Тестовые записи группы 1',
                author=cls.user1,
                group=cls.group1,
            )
        
        # create test posts in group 2
        for post in range(10):
            cls.post = Post.objects.create(
                text='Тестовые записи группы 2',
                author=cls.user2,
                group=cls.group2,
            )
        
        # templates and pages
        def test_pages_uses_correct_template(self):
            """URL-адрес использует соответствующий шаблон."""
            # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
            templates_pages_names = {
                reverse('posts:index'): 'posts/index.html',
                reverse('posts:post_create'): 'posts/create.html',
                reverse('posts:group_list', 
                        kwargs={'slug': 'test-slug'}): ('posts/group_list.html'),
                reverse('posts:profile',
                        kwargs={'username': 'User'}): ('posts/profile.html'),
                reverse('posts:post_detail',
                        kwargs={'post_id': 15}): ('posts/post_detail.html'),
                reverse('posts:post_edit',
                        kwargs={'post_id': 14}): ('posts/create.html'),
                
            }
        
            # check pages and views
            for reverse_name, template in templates_pages_names.items():
                with self.subTest(reverse_name=reverse_name):
                    response = self.authorized_client.get(reverse_name)
                    self.assertTemplateUsed(response, template)
