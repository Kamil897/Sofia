#!/usr/bin/env python3
"""
Скрипт для запуска телеграм-бота Sofia Coffee
"""

import os
import sys
import django
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Загружаем переменные из .env файла
env_file = project_root / '.env'
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sofia_coffee.settings')
django.setup()

# Импортируем и запускаем бота
from telegram_bot.bot import main
import asyncio

if __name__ == "__main__":
    print("🚀 Запуск Sofia Coffee Telegram Bot...")
    print("📝 Убедитесь, что установлен токен бота в переменной окружения TELEGRAM_BOT_TOKEN")
    print("🛑 Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
