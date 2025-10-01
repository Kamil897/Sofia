import os
from django.conf import settings

# Настройки для телеграм-бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-domain.com/webhook/')

# Настройки Django для интеграции с ботом
DJANGO_SETTINGS_MODULE = 'sofia_coffee.settings'
