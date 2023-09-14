import pytest
from rest_framework.test import APIClient
import json
import os
from backend.models import User, FileU
from dotenv import load_dotenv
import random

load_dotenv()
class TestApi:

    def __init__(self, client):
        self.client = client
        self.user_d = {}
        self.USER_INFO = {'username': 'Ivan',
                          'password': 'fddf44787dfew'
                          }

    "Тест регистрации, подтверждения почты и входа в систему"
    def test_user_register(self):
        """
        Регистрация
        """
        response = self.client.post('/register/',
                                    data=self.USER_INFO)
        r = response.json()
        assert response.status_code == 200
        assert r['Status'] is True
        """
        Вход в систему
        """
        response = self.client.post('/login/',
                                    data=self.USER_INFO)
        r = response.json()
        self.user_d['token'] = r['Token']
        self.user_d['user_id'] = r['user_id']
        assert response.status_code == 200
        assert r['Status'] is True
        assert len(r['Token']) > 0


    def test_accoun_details_get_put(self):
        """Получение данных пользователя"""
        url = f"/user/{self.user_d['user_id']}/"
        response = self.client.get(url,
                                   headers={'Authorization': f'Token {self.user_d["token"]}'})
        r = response.json()
        assert response.status_code == 200
        assert r['username'] == self.USER_INFO["username"]
        """Редоктировать данные пользователя"""
        url = f"/user/{self.user_d['user_id']}/"
        new_username = 'ne_ivan'
        response = self.client.put(url,
                                   data={'username': new_username},
                                   headers={'Authorization': f'Token {self.user_d["token"]}'})
        r = response.json()
        assert response.status_code == 200
        assert r['username'] == new_username
        """Будет ли ошибка при неверном токене"""
        response = self.client.get('/user/',
                                   headers={'Authorization': f'Token {random.uniform(0, 20)}'})

        assert response.status_code == 401

    def test_file_get_post_del(self):
        """Загрузить файл"""
        url = f"/user/{self.user_d['user_id']}/"
        response = self.client.post(url,
                                   headers={'Authorization': f'Token {self.user_d["token"]}'})
        r = response.json()
        assert response.status_code == 200



@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_action(client):
    obj = TestApi(client)
    obj.test_user_register()
    obj.test_accoun_details_get_put()
