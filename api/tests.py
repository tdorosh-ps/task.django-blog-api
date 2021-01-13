from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Post


class PostsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        user = User.objects.create(username='user', password='password')
        token = Token.objects.create(user=user)
        cls.api_client = APIClient()
        cls.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        for i in range(1, 4):
            Post.objects.create(title=f'Test title {i}', body=f'Body for post {i}', owner=user)
        super().setUpClass()

    def test_post_list(self):
        response = self.api_client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), len(response.data))

    def test_post_create(self):
        data = {
            'title': 'My first test post',
            'body': 'Body for my first test post'
        }
        response = self.api_client.post(reverse('post-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['title'], response.data['title'])
        self.assertEqual(data['body'], response.data['body'])

    def test_post_retrieve(self):
        post = Post.objects.order_by("?").first()
        response = self.api_client.get(reverse('post-retrieve', args=[post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.id, response.data['id'])

    def test_post_add_comment(self):
        post = Post.objects.order_by("?").first()
        data = {
            'body': f'Body for my {post.id} test post'
        }
        response = self.api_client.post(reverse('post-add-comment', args=[post.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['body'], response.data['body'])
        post.refresh_from_db()
        self.assertEqual(data['body'], post.comments.first().body)