# Foodgram Project
<a name="Начало"></a>
[![Foodgram workflow](https://github.com/dmsnback/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/dmsnback/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

- [Описание](#Описание)
- [Технологии](#Технологии)
- [Шаблон заполнения .env-файла](#Шаблон)
- [Запуск проекта на локальной машине](#Запуск)
- [Запуск проекта на боевом сервере](#Запуск2)
- [Авторы](#Авторы)

#

<a name="Описание"></a>
### Описание

Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.

```
Проект адаптирован для использования PostgreSQL и развёртывания в контейнерах Docker.
Также используютя инструменты CI/CD.
```
[Вернуться в начало](#Начало)

<a name="Технологии"></a>
### Технологии

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/ru/)
[![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org)

[Вернуться в начало](#Начало)

<a name="Шаблон"></a>
### Шаблон заполнения .env-файла, расположен по пути infra/.env
##### (в settings.py указаны дефолтные значения для переменных из env-файла)
```python
SECRET_KEY = 'Ваш секретный ключ'

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
[Вернуться в начало](#Начало)

<a name="Запуск"></a>
## Запуск проекта на локальной машине:

- Склонируйте репозиторий
```python
git clone git@github.com:dmsnback/foodgram-project-react.git
```

- Переходим в папку с файлом ```docker-compose.yaml```
```python
cd infra
```

- Запускаем Docker контейнеры
```python
docker-compose up -d --build
```

- Выполняем миграции
```python
docker-compose exec backend python manage.py migrate 
```

- Создаём суперюзера
```python
docker-compose exec backend python manage.py createsuperuser
```

- Собираем статику
```python
docker-compose exec backend python manage.py collectstatic --no-input
```
- Наполняем базу данных содержимым из файла ```ingredients.csv```:
```python
docker-compose exec backend python manage.py load_ingredients
```
#### Проект станет доступен по адресу 

[http://localhost/recipes](http://localhost/recipes)

#### Документация к API будет доступна по адресу

[http://localhost/api/docs/](http://localhost/api/docs/)

В документации описано, как должен работать ваш API. Документация представлена в формате Redoc.

[Вернуться в начало](#Начало)

#
<a name="Запуск2"></a>
## Запуск проекта на боевом сервере:

#### При пуше в ветку main код автоматически проверяется, тестируется и деплоится на сервер

- Склонируйте репозиторий
```python
git clone git@github.com:dmsnback/foodgram-project-react.git
```
- Зайдите на удалённый сервер

- Обновите существующий список пакетов:
```python
sudo apt update
```
- Установите Docker на сервер:
```python
sudo apt install docker.io 
```
- Установите docker-compose на сервер:
```python
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- Затем необходимо задать правильные разрешения, чтобы сделать команду docker-compose исполняемой:
```python
sudo chmod +x /usr/local/bin/docker-compose
```
- Чтобы проверить успешность установки, запустите следующую команду:
```python
sudo docker-compose --version
```
Вывод будет выглядеть следующим образом:
```python
docker-compose version 1.29.2, build unknown
```
- Локально отредактируйте файл ```infra/nginx.conf```, в строке ```server_name``` вписать IP-адрес или доменное имя сервера.

- Скопируйте файлы docker-compose.yaml и nginx/nginx.conf из вашего проекта на сервер в ```home/<ваш_username>/docker-compose.yaml``` и ```home/<ваш_username>/nginx.conf``` соответственно.
```python
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp default.conf <username>@<host>:/home/<username>/nginx.conf
```
- Для работы с ```Workflow``` добавить в ```Secrets GitHub``` переменные окружения для работы:
```python
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД

DOCKER_USERNAME= #имя пользователя
DOCKER_PASSWORD= #пароль от DockerHub

USER= #username для подключения к серверу
HOST= #IP сервера
PASSPHRASE= #пароль для сервера, если он установлен
SSH_KEY= #ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)

TELEGRAM_TO= #ID чата, в который придет сообщение
TELEGRAM_TOKEN= #токен вашего бота
```

___По команде ```git push``` запускается скрипт ```GitHub actions``` который выполняет автоматический deploy на сервер___


- <u>__Workflow состоит из пяти шагов__:</u>

	- Проверка кода на соответствие стандарту ```PEP8```.
	
	- Сборка и доставка докер-образа для контейнера ```backend``` на ```Docker Hub```.
	- Сборка и доставка докер-образа для контейнера ```frontend``` на ```Docker Hub```.
	
	- Автоматический деплой проекта на боевой сервер.
	
	- Отправка уведомления в ```Telegram``` о том, что процесс деплоя успешно завершился.

- После сборки контейнера зайдите на сервер и выполните следующие команды:
```python
# Выполняем миграции
sudo docker-compose exec backend python manage.py migrate

# Создаем суперппользователя
sudo docker-compose exec backend python manage.py createsuperuser

# Собираем статику со всего проекта
sudo docker-compose exec backend python manage.py collectstatic --no-input

# Наполняем базу данных содержимым из файла ingredients.csv
sudo docker-compose exec backend python manage.py load_ingredients
```

#### Проект станет доступен по адресу:

```<ваш_ip-адрес_или_домен>/recipes```

#### Документация к API: 

```<ваш_ip-адрес_или_домен>/api/docs/```

В документации описано, как должен работать ваш API. Документация представлена в формате Redoc.

[Вернуться в начало](#Начало)


<a name="Авторы"></a>
## Автор backend  части:


- [Титенков Дмитрий](https://github.com/dmsnback)

[Вернуться в начало](#Начало)
