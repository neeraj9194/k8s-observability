from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Article


# Create your tests here.

class TestArticleApi(TestCase):

    def auth(self, username, password):
        self.client = APIClient()
        self.client.login(username=username, password=password)
        return super().setUp()

    def setUp(self) -> None:
        self.client = None
        self.test_user = User.objects.create_user(
            'testuser', 'test@test.com', 'testpass')
        self.new_article = {
            "title": "New Article",
            "read_time": 1,
            "published": False,
            "content": "Hello world!",
            "author_id": self.test_user.id
        }

    def test_create_article(self):
        self.auth('testuser', 'testpass')
        response = self.client.post('/api/article/', self.new_article)
        self.assertEqual(201, response.status_code)
        self.assertEqual(Article.objects.count(), 1)

    def test_retrieve_article(self):
        self.auth('testuser', 'testpass')
        article = Article.objects.create(title="first")
        response = self.client.get(f'/api/article/{article.id}/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(Article.objects.count(), 1)
