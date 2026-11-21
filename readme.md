# YaCut — сервис укорачивания ссылок

Проект представляет собой веб-сервис, который позволяет пользователям создавать короткие ссылки для длинных URL-адресов. 
Дополнительной функцией является возможность асинхронной загрузки файлов на Яндекс Диск с генерацией коротких ссылок для скачивания.

### Стек технологий:
* Python 3.12
* Flask (с поддержкой async views)
* SQLAlchemy + Flask-Migrate (ORM и миграции)
* WTForms + Flask-WTF (формы и валидация)
* aiohttp (асинхронные запросы к API Яндекс Диска)
* Yandex Disk API
* Bootstrap (фронтенд)

### Как развернуть проект:

1. Клонировать репозиторий и перейти в него:
   git clone <ссылка_на_репозиторий>
   cd async-yacut

2. Создать и активировать виртуальное окружение:

python3 -m venv venv
Для Linux/macOS: source venv/bin/activate

Для Windows: source venv/Scripts/activate

3. Установить зависимости:

python -m pip install --upgrade pip
pip install -r requirements.txt


4. Создать файл .env в корне проекта и заполнить переменные окружения:

env
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=your_super_secret_key
DISK_TOKEN=your_yandex_disk_oauth_token
(Токен для Яндекс Диска можно получить в консоли разработчика Яндекс ID)

5. Применить миграции для создания базы данных:

bash
flask db upgrade


6. Запустить проект:

bash
flask run


Автор:
ArtemShastunov