import pytest
from rest_framework.test import APIClient
from dotenv import load_dotenv
import random

load_dotenv()


class TestApi:
    def __init__(self, client):
        self.client = client
        self.user_d = {}
        self.USER_INFO = {"username": "Ivan", "password": "fddf44787dfew"}

    "Тест регистрации, подтверждения почты и входа в систему"

    def test_user_register(self):
        """
        Регистрация
        """
        # отправляем запрос на регистрацию
        response = self.client.post("/api/v1/register/", data=self.USER_INFO)
        r = response.json()
        # проверяем стату код
        assert response.status_code == 200
        # проверяем что не получили ошибку.
        # ответ: Status True, регистрация прошла успешно
        assert r["Status"] is True
        """
        Вход в систему
        """
        # отправляем запрос на получение токена
        response = self.client.post("/api/v1/login/", data=self.USER_INFO)
        r = response.json()
        # формируем словарь с полученым токеном и user_id,
        # для дальнейшего тестирования
        self.user_d["token"] = r["Token"]
        self.user_d["user_id"] = r["user_id"]
        # проверяем стату код
        assert response.status_code == 200
        # ответ: Status True, авторизация прошла успешно
        assert r["Status"] is True
        # проверяем наличие токена
        assert r["Token"]
        assert len(r["Token"]) > 0

    def test_accoun_details_get_put(self):
        """Получение данных пользователя"""

        # формируем url
        # url для получения всех пользователей: /user/
        url = f"/api/v1/user/{self.user_d['user_id']}/"
        # отправляем запрос на получение данных одного пользователя,
        response = self.client.get(
            url, headers={"Authorization": f'Token {self.user_d["token"]}'}
        )
        r = response.json()
        # проверяем стату код
        assert response.status_code == 200
        # проверяем имя пользователя. Имя пользователя в бд уникальное
        assert r["username"] == self.USER_INFO["username"]

        """Редоктировать данные пользователя"""
        # формируем url
        url = f"/api/v1/user/{self.user_d['user_id']}/"
        # создаем новое имя для пользователя
        new_username = "ne_ivan"
        # отправляем запрос на изменение имени
        response = self.client.put(
            url,
            data={"username": new_username},
            headers={"Authorization": f'Token {self.user_d["token"]}'},
        )
        r = response.json()
        # проверяем стату код
        assert response.status_code == 200
        # проверяем что имя изменилось
        assert r["username"] == new_username
        """Будет ли ошибка при неверном токене"""
        # отправляем запрос на получение данных пользователей с несуществующим токеном
        response = self.client.get(
            "/api/v1/user/", headers={"Authorization": f"Token {random.uniform(0, 20)}"}
        )
        # проверяем стату код
        assert response.status_code == 401

    def test_file_get_post_del(self):
        """Загрузить файл"""
        # формируем url
        url = f"/api/v1/UploadViewFile/"
        # открываем файл
        file = open("3.csv", "rb")
        # отправляем запрос на загрузку файла
        response = self.client.post(
            url,
            data={"file": file},
            headers={"Authorization": f'Token {self.user_d["token"]}'},
        )
        r = response.json()
        # закрываем файл
        file.close()
        # добовляем в словарь id файла для дальнейших тестов
        self.user_d["user_file"] = r["id"]
        # проверяем стату код
        assert response.status_code == 201
        # проверяем наличее id файла
        assert r["id"]
        # проверяем что колонки файла сформированны в отдельный список
        assert len(r["column_file"]) > 0
        # проверяем что создатель файла создон корректно
        assert r["user"] == self.user_d["user_id"]

        """Просмотреть файлы"""
        # формируем url
        url = f"/api/v1/UploadViewFile/"
        response = self.client.get(
            url, headers={"Authorization": f'Token {self.user_d["token"]}'}
        )
        r = response.json()
        # проверяем что ответ не пустой
        assert len(r) > 0
        assert r[0]["id"] == self.user_d["user_file"]

        """Просмотреть конкретный файл"""
        # формируем url с id файла
        url = f"/api/v1/UploadViewFile/{self.user_d['user_file']}/"
        response = self.client.get(
            url, headers={"Authorization": f'Token {self.user_d["token"]}'}
        )
        r = response.json()
        # проверяем что id файла == id запроса
        assert r["id"] == self.user_d["user_file"]
        assert r["user"] == self.user_d["user_id"]
        """Удалить файл"""

        # Ошибка при удалении если пользователь не владелец
        url = f"/api/v1/UploadViewFile/{self.user_d['user_file']}/"
        response = self.client.delete(
            url, headers={"Authorization": f"Token {random.uniform(0, 20)}"}
        )
        # проверяем стату код
        assert response.status_code == 401

        # Удаление
        url = f"/api/v1/UploadViewFile/{self.user_d['user_file']}"
        response = self.client.delete(
            url, headers={"Authorization": f'Token {self.user_d["token"]}'}
        )
        # проверяем стату код
        assert response.status_code == 301


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_action(client):
    obj = TestApi(client)
    obj.test_user_register()
    obj.test_accoun_details_get_put()
    obj.test_file_get_post_del()
