from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from tasks.models import Task

from django.contrib.auth.models import User

import json

class CreateTaskTestCase(TestCase):
    def setUp(self):    
        user = User(
            username = 'testing_login@testing.com',
        )
        user.set_password('testing123')
        user.save()

        self.client_login = APIClient()
        response_login = self.client_login.post(
            '/login/', {
                "username": "testing_login@testing.com",
                "password": "testing123"
            },
            format='json'
        )
        result = json.loads(response_login.content)

        self.client_login.credentials(HTTP_AUTHORIZATION='Bearer ' + result['access'])
    
    def test_create_task(self):
        client = self.client_login

        response_create_task = client.post(
            '/tasks/', {
                "title": "testing_create_task",
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )

        response_get_task = client.get(
            '/tasks/', {
            },
            format='json'
        )

        self.assertEqual(response_create_task.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get_task.data[0]['title'], 'testing_create_task')
        self.assertEqual(response_get_task.data[0]['description'], 'testing_create_task')
        self.assertEqual(response_get_task.data[0]['complete'], False)
        self.assertEqual(response_get_task.data[0]['expiration_date'], '2020-12-12T12:12:12Z')

    def test_create_task_without_token(self):
        client = self.client_login

        client.credentials()

        response_create_task = client.post(
            '/tasks/', {
                "title": "testing_create_task",
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )
        self.assertEqual(response_create_task.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_create_task.data['detail'], 'Authentication credentials were not provided.')
    
    def test_create_task_with_invalid_token(self):
        client = self.client_login

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response_create_task = client.post(
            '/tasks/', {
                "title": "testing_create_task",
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )
        self.assertEqual(response_create_task.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_create_task.data['detail'], 'Given token not valid for any token type')

    def test_create_task_with_no_title(self):
        client = self.client_login

        response_create_task = client.post(
            '/tasks/', {
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )
        self.assertEqual(response_create_task.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_create_task.data['title'][0], 'This field is required.')

    def test_create_task_with_too_long_title(self):
        client = self.client_login

        response_create_task = client.post(
            '/tasks/', {
                "title": "testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task_testing_create_task__",
                "description": "testing_create_task",
                "complete": False,
                "expiration_date": "2020-12-12 12:12:12"
            },
            format='json'
        )
        self.assertEqual(response_create_task.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_create_task.data['title'][0], 'Title is too long.')


