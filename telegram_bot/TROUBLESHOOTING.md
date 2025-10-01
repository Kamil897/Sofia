# Устранение неполадок телеграм-бота

## Частые проблемы и их решения

### 1. Ошибка "SynchronousOnlyOperation"

**Проблема:**
```
SynchronousOnlyOperation: You cannot call this from an async context - use a thread or sync_to_async.
```

**Причина:** Попытка использовать Django ORM (синхронные операции с БД) внутри асинхронных функций aiogram.

**Решение:** Используйте `sync_to_async` для обертки Django операций:

```python
from asgiref.sync import sync_to_async

@sync_to_async
def get_all_products():
    return list(Product.objects.all())

# Использование в асинхронной функции:
async def show_menu(message):
    products = await get_all_products()  # await обязательно!
```

### 2. Ошибка "Token is invalid!"

**Проблема:**
```
aiogram.utils.token.TokenValidationError: Token is invalid!
```

**Причины:**
- Токен скопирован не полностью
- В токене есть лишние пробелы
- Токен устарел или отозван

**Решение:**
1. Получите новый токен у [@BotFather](https://t.me/botfather)
2. Скопируйте токен полностью (должен начинаться с цифр и содержать двоеточие)
3. Обновите файл `.env`

### 3. Бот не отвечает на команды

**Возможные причины:**
- Django-сервер не запущен
- Проблемы с подключением к базе данных
- Бот не запущен или упал с ошибкой

**Решение:**
1. Убедитесь, что Django-сервер работает:
   ```bash
   python manage.py runserver
   ```
2. Проверьте логи бота на наличие ошибок
3. Перезапустите бота

### 4. Ошибка "ModuleNotFoundError: No module named 'django'"

**Проблема:** Django не установлен

**Решение:**
```bash
pip install -r requirements.txt
```

### 5. Ошибка подключения к базе данных

**Проблема:**
```
django.db.utils.OperationalError: no such table: shop_product
```

**Решение:**
```bash
python manage.py migrate
```

### 6. Проблемы с кодировкой файла .env

**Проблема:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff
```

**Решение:**
1. Удалите файл `.env`
2. Создайте новый файл с правильной кодировкой:
   ```bash
   echo TELEGRAM_BOT_TOKEN=your_token_here > .env
   ```

## Отладка

### Включение подробных логов

Добавьте в начало `bot.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Проверка подключения к базе данных

Создайте тестовый скрипт `test_db.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sofia_coffee.settings')
django.setup()

from shop.models import Product

products = Product.objects.all()
print(f"Найдено товаров: {products.count()}")
for product in products:
    print(f"- {product.name}: {product.price} ₽")
```

Запустите:
```bash
python test_db.py
```

## Полезные команды

### Проверка статуса Django
```bash
python manage.py check
```

### Создание суперпользователя
```bash
python manage.py createsuperuser
```

### Просмотр миграций
```bash
python manage.py showmigrations
```

### Сброс базы данных (осторожно!)
```bash
rm db.sqlite3
python manage.py migrate
```

## Контакты

Если проблемы не решаются, проверьте:
1. Версии Python и Django
2. Логи ошибок
3. Настройки базы данных
4. Сетевые подключения
