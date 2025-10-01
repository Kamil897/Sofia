#!/usr/bin/env python3
"""
Скрипт для добавления тестовых данных в базу данных
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sofia_coffee.settings')
django.setup()

from shop.models import Category, Product, News, Review, Promo
from django.utils import timezone
from datetime import timedelta

def create_test_data():
    print("🔄 Создание тестовых данных...")
    
    # Создаем категории
    coffee_category, created = Category.objects.get_or_create(
        name="Кофе",
        defaults={'slug': 'coffee'}
    )
    
    desserts_category, created = Category.objects.get_or_create(
        name="Десерты", 
        defaults={'slug': 'desserts'}
    )
    
    print(f"✅ Категории созданы: {coffee_category.name}, {desserts_category.name}")
    
    # Создаем товары
    products_data = [
        {
            'name': 'Латте',
            'description': 'Нежный кофе с молоком и пенкой',
            'price': 150.00,
            'category': coffee_category
        },
        {
            'name': 'Капучино',
            'description': 'Классический кофе с молочной пенкой',
            'price': 140.00,
            'category': coffee_category
        },
        {
            'name': 'Американо',
            'description': 'Черный кофе без молока',
            'price': 120.00,
            'category': coffee_category
        },
        {
            'name': 'Тирамису',
            'description': 'Итальянский десерт с кофе и маскарпоне',
            'price': 200.00,
            'category': desserts_category
        },
        {
            'name': 'Чизкейк',
            'description': 'Нежный сырный торт с ягодным соусом',
            'price': 180.00,
            'category': desserts_category
        }
    ]
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"✅ Товар создан: {product.name} - {product.price} ₽")
        else:
            print(f"ℹ️ Товар уже существует: {product.name}")
    
    # Создаем новости
    news_data = [
        {
            'title': 'Новое меню весны!',
            'text': 'Мы рады представить вам обновленное весеннее меню с новыми вкусами и сезонными напитками.'
        },
        {
            'title': 'Скидка 20% на все десерты',
            'text': 'Специальное предложение: скидка 20% на все десерты при заказе от 500 рублей.'
        }
    ]
    
    for news_item_data in news_data:
        news_item, created = News.objects.get_or_create(
            title=news_item_data['title'],
            defaults=news_item_data
        )
        if created:
            print(f"✅ Новость создана: {news_item.title}")
    
    # Создаем отзывы
    reviews_data = [
        {
            'customer_name': 'Анна',
            'text': 'Отличный кофе и уютная атмосфера! Обязательно вернусь снова.',
            'rating': 5
        },
        {
            'customer_name': 'Михаил',
            'text': 'Тирамису просто восхитительный! Рекомендую всем сладкоежкам.',
            'rating': 5
        },
        {
            'customer_name': 'Елена',
            'text': 'Хорошее место для работы. Wi-Fi быстрый, кофе вкусный.',
            'rating': 4
        }
    ]
    
    for review_data in reviews_data:
        review, created = Review.objects.get_or_create(
            customer_name=review_data['customer_name'],
            text=review_data['text'],
            defaults=review_data
        )
        if created:
            print(f"✅ Отзыв создан: {review.customer_name} - {review.rating}/5")
    
    # Создаем промо-акцию
    promo, created = Promo.objects.get_or_create(
        name='Скидка на кофе',
        defaults={
            'description': 'Скидка 15% на все виды кофе при заказе от 300 рублей',
            'discount': 15.00,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=30)
        }
    )
    if created:
        print(f"✅ Промо-акция создана: {promo.name}")
    
    print("\n🎉 Тестовые данные успешно созданы!")
    print(f"📊 Статистика:")
    print(f"   - Категорий: {Category.objects.count()}")
    print(f"   - Товаров: {Product.objects.count()}")
    print(f"   - Новостей: {News.objects.count()}")
    print(f"   - Отзывов: {Review.objects.count()}")
    print(f"   - Промо-акций: {Promo.objects.count()}")

if __name__ == "__main__":
    create_test_data()
