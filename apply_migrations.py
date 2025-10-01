#!/usr/bin/env python3
"""
Скрипт для применения миграций Django
"""

import os
import django
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sofia_coffee.settings')
django.setup()

def apply_migrations():
    print("🔄 Создание миграций...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("🔄 Применение миграций...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Миграции успешно применены!")

if __name__ == "__main__":
    apply_migrations()
