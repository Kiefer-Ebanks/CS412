# File: tests.py
# Author: Kiefer Ebanks (kebanks@bu.edu), 4/7/2026
# Description: The tests for the mini instagram app and the API endpoints

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Profile

class UserTests(APITestCase):

    def test_register_user(self):
        ''' test the register user API endpoint '''

        url = reverse('api_register')
        data = {'username': 'testuser', 'password': 'testpass123', 'email': 'testuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_user(self):
        ''' test the login user API endpoint '''

        user = User.objects.create_user(username='testuser', password='testpass123')
        Profile.objects.create(
            user=user,
            username='testuser',
            display_name='Test User',
            bio_text='',
        )

        url = reverse('api_login')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('profile_id', response.data)
        self.assertIn('profile', response.data)
