#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы корзины
"""

# Имитируем функции корзины
user_carts = {}

def get_user_cart_items(user_id):
    """Получить товары в корзине пользователя"""
    print(f"DEBUG: get_user_cart_items вызвана для пользователя {user_id}")
    print(f"DEBUG: Полная корзина: {user_carts}")
    
    if user_id not in user_carts:
        print(f"DEBUG: Пользователь {user_id} не найден в корзине")
        return []
    
    cart_items = []
    for product_id, quantity in user_carts[user_id].items():
        cart_items.append({
            'product_id': int(product_id),  # Преобразуем в int
            'quantity': quantity,
            'product': None  # Будет загружено отдельно
        })
    
    print(f"DEBUG: Возвращаем {len(cart_items)} товаров для пользователя {user_id}")
    return cart_items

def add_to_cart_db(user_id, product_id, quantity=1):
    """Добавить товар в корзину"""
    print(f"DEBUG: add_to_cart_db вызвана с user_id={user_id}, product_id={product_id}, quantity={quantity}")
    
    if user_id not in user_carts:
        user_carts[user_id] = {}
        print(f"DEBUG: Создана новая корзина для пользователя {user_id}")
    
    if product_id in user_carts[user_id]:
        user_carts[user_id][product_id] += quantity
        print(f"DEBUG: Увеличено количество товара {product_id} до {user_carts[user_id][product_id]}")
    else:
        user_carts[user_id][product_id] = quantity
        print(f"DEBUG: Добавлен новый товар {product_id} с количеством {quantity}")
    
    print(f"DEBUG: Итоговая корзина пользователя {user_id}: {user_carts[user_id]}")
    return True

def test_cart():
    """Тестирование корзины"""
    print("🧪 Тестирование корзины...")
    
    user_id = 123456789
    product_id = 1
    
    # Тест 1: Добавление товара
    print("\n1. Добавление товара в корзину:")
    add_to_cart_db(user_id, product_id, 1)
    
    # Тест 2: Получение товаров из корзины
    print("\n2. Получение товаров из корзины:")
    cart_items = get_user_cart_items(user_id)
    print(f"Результат: {cart_items}")
    
    # Тест 3: Проверка пустой корзины
    print("\n3. Проверка пустой корзины:")
    empty_cart = get_user_cart_items(999999999)
    print(f"Результат: {empty_cart}")
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    test_cart()
