from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.


class TestAccountApi(TestCase):

    def auth(self, username, password):
        self.client.login(username=username, password=password)
        return super().setUp()

    def setUp(self) -> None:
        self.client = APIClient()
        self.test_user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.new_user = {
            'username': 'test1', 
            'email': 'teat@gmail.com', 
            'first_name': 'test', 
            'last_name': 'T'
        }

    def test_create_user(self):
        self.auth('testuser', 'testpass')
        response = self.client.post('/api/user/', self.new_user)
        self.assertEqual(201, response.status_code)
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_not_auth(self):
        response = self.client.post('/api/user/', self.new_user)
        self.assertEqual(403, response.status_code)
        self.assertEqual(User.objects.count(), 1)

    def test_retrieve_user(self):
        self.auth('testuser', 'testpass')
        resp_dict = self.new_user = {
            'id': self.test_user.id,
            'username': 'testuser', 
            'email': 'test@test.com', 
            'first_name': '', 
            'last_name': ''
        }
        response = self.client.get(f'/api/user/{self.test_user.id}/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(resp_dict, response.data)
