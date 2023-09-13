# API сервис для работы с импортируемыми данными.

Установка:
1. Клонировать репозиторий:
```
git clone https://github.com/swan-007/test_assignment_HTTP_service.git
```
2. Прейти в каталог HTTP_service:
```
cd HTTP_service 
```    
3. Установить зависимости:
 ```
 pip install -r requirements.txt
 ```
4. Создать файл .env со следующими полями 
 ```
 (SECRET_KEY, DEBUG, ALLOWED_HOST, DB_ENGINE, DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD)
 ```
5. Применить миграции:
 ```
 python manage.py migrate 
 ```  
6. Запуск сервера:
 ```
 python manage.py runserver
 ```
   

### Использование:

1. Регистрация. 
   #### Метод  POST   
   - url: ```****/register/``` 
   - Обязательные параметры: ```username, password```  
   - Пример запроса: ```Body={"username": "Ivan","password": qwerty123 }```
   - Пример ответа: ```{"Status": true}``` 
   



2. Вход.
   #### Метод  POST   
   - url: ```****/login/``` 
   - Обязательные параметры: ```username, password```  
   - Пример запроса: ```Body={"username": "Ivan","password": qwerty123 }```
   - Пример ответа: ```{"Status": true, "Token": "e1b9fb2048d15f31aded9238c353729440de9012"
}``` 
2. Работа с данными пользователя.
   #### Получить всех или конкретного пользователя
   #### Метод  GET  
   - url: ```****/user/``` 
   - Обязательные параметры: ```Authorization token```  
   - Пример запроса: ```Headers={Authorization: Token полученный токен}``` 
   - Пример ответа:```[{"id": 1,"username": "test"}, {"id": 2,"username": "testtest"}]``` 
   - Фильтрация по id и username. Пример : url: ```****/user/id/``` 
   #### Поменять имя пользователя
   #### Метод  POST
   - url: ```****/user/id/``` 
   - Обязательные параметры: ```Authorization token```  
   - Пример запроса: ```Body={"username": "Ivan"} Headers={Authorization: Token полученный токен}``` 
   - Пример ответа:```[{"id": 1,"username": "Ivan"}}]```

3. Загрузить файл, просмотреть список файлов.
   #### Просмотреть список файлов или конкретный файл:
   #### Метод  GET  
   - url: ```****/UploadViewFile/``` 
   - Обязательные параметры: ```Authorization token```  
   - Пример запроса: ```Headers={Authorization: Token полученный токен}``` 
   - Пример ответа:```[{"id":5,"created_data":"2023-09-13","file":"http://127.0.0.1:8000/3_7IQ59hu.csv","user":1,"column_file":"['hostname', 'vendor', 'model', 'location']"}]``` 
   - Фильтрация по id и user. Пример : url: ```****/UploadViewFile/id/``` 
   #### Загрузить файл : 
   #### Метод  POST
   - url: ```****/user/``` 
   - Обязательные параметры: ```user, file, Authorization token```  
   - Пример запроса: ```Body={"user": "1", 'file': '3.csv' } Headers={Authorization: Token полученный токен}``` 
   - Пример ответа:```{"id":6,"created_data":"2023-09-13T14:56:49.353988Z","file":"http://127.0.0.1:8000/3_Eanop0s.csv","user":1,"column_file":"['hostname', 'vendor', 'model', 'location']"}```
   #### Удалить файл : 
   #### Метод  DELETE
   - Удалить файл может только его владелец
   - url: ```****/UploadViewFile/id_записи/``` 
   - Обязательные параметры: ```Authorization token```  
   - Пример запроса: ```Headers={Authorization: Token полученный токен}``` 
   - Пример ответа:```[]```
4. Для работы с файлами.
   #### Метод  GET  
   - url: ```****/UploadViewFile/``` 
   - Обязательные параметры: ``` id_записи, Authorization token```
     - Опциональная фильтрация и сортировка.
                    - параметры :  column_name, desired_value, sort_by(может быть несколько)
                    - Опциональная фильтрация
                    - Опциональная сортировка
                     
   - Пример запроса: ```Body={"id": "1", 'desired_value': 'Liverpool', 'column_name': 'location', 'sort_by': 'vendor'}  Headers={Authorization: Token полученный токен}``` 
   - Пример ответа:```[{"hostname":"sw3","vendor":"Cisco","model":3650,"location":"Liverpool"},{"hostname":"sw2","vendor":"Cisco","model":3850,"location":"Liverpool"}]``` 
   