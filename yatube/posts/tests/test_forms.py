from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from posts.models import Group, Post, User
from posts.forms import PostForm
from http import HTTPStatus

class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create a non-authorized
        cls.guest_client = Client()
        # create an authorized client
        cls.user = User.objects.create_user(username='user')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        
        # create group in DB
        cls.group = Group.objects.create(
            title='Title for post',
            slug='test-slug',
            description='Description for group'
        )
        
        # create post in DB
        cls.post = Post.objects.create(
            text='Text for post',
            author=cls.user,
            group=cls.group
        )
        cls.form = PostForm()
        

    def test_post_create(self):
        """При отправке валидной формы создается запись"""
        # amount of posts
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Text for post',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # checking redirect
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': PostCreateFormTests.user})
        )
        # checking amount of posts
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # checking existence of the new post
        self.assertTrue(
            Post.objects.filter(
                group=PostCreateFormTests.group,
                author=PostCreateFormTests.user,
                text='Text for post'
            ).exists()
        )

