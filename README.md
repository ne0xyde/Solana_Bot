# Telegram бот на aiogram для сети Solana

```
Этот базовая версия Telegram бота на фреймворке aiogram 3.7.0 с интеграцией базы данных MYSQL
Работа в сети Solana происходит через API проекта https://tatum.io

Бот также включает простую админ-панель для просмотра добавленных пользователей и функционал профиля пользователя, позволяющий просматривать количество приглашенных
пользователей и получать реферальную ссылку.
```

## Установка

Для установки необходимых зависимостей выполните следующие команды:

```bash
pip install -r requirements.txt
```

где requirements.txt содержит следующие зависимости:

``` requirements
aiogram~=3.7.0
python-decouple~=3.8
asyncmy~=0.2.9
sqlalchemy~=2.0.31
```

## Использование

Чтобы запустить бота, выполните следующие шаги:

``` bash
pip install -r requirements.txt
```

Создайте файл .env в корне проекта и добавьте в него следующие переменные:

``` textmate
TOKEN=your_bot_token
ADMINS=admin1_id,admin2_id
TATUM_API-KEY=your_tatum.io_api_key
MYSQL_ASYNCMY_LINK=mysql+asyncmy://username:password@host:port/dbname
``` 

Замените данные на свои. Предварительно не забудьте узнать свой телеграмм ID, развернуть базу данных и создать токен
бота.

## Запустите бота:

``` bash
python aiogram_run.py
``` 

## Структура проекта

```markdown
- db_handler
    - __init__.py: Инициализация модуля.
    - db_funk.py: Функции для взаимодействия с базой MYSQL.

- handlers
    - __init__.py: Инициализация модуля.
    - admin_panel.py: Роутер для админ-панели.
    - user_router.py: Роутер для пользовательской части.

- keyboards
    - __init__.py: Инициализация модуля.
    - kbs.py: Файл со всеми клавиатурами.
  
- solana
    - __init__.py: Инициализация модуля.
    - solana_wallet.py: Функции для взаимодействия с сетью Solana через API tatum.io.  

- utils
    - __init__.py: Инициализация модуля.
    - utils.py: Файл с утилитами.
```

### Корневые файлы проекта

```markdown
- .env: Файл с переменными окружения для конфигурации.
- aiogram_run.py: Главный файл для запуска бота.
- create_bot.py: Файл с настройками бота.
- requirements.txt: Файл с зависимостями проекта.
- run_bot.py: Файл для запуска бота через systemd.
```

# Лицензия

Проект лицензирован под MIT License.

Форк проекта easy_referer_bot-master