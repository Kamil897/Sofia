import os
import django
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import asyncio
from asgiref.sync import sync_to_async
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sofia_coffee.settings')
django.setup()

from shop.models import Product, Order, OrderItem, Category, Cart

# Асинхронные обертки для Django ORM
@sync_to_async
def get_all_categories():
    return list(Category.objects.all())

@sync_to_async
def get_products_by_category(category_id):
    return list(Product.objects.filter(category_id=category_id))

@sync_to_async
def get_all_products():
    return list(Product.objects.all())

@sync_to_async
def get_product_by_id(product_id):
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None

@sync_to_async
def create_order_db(customer_name, phone):
    return Order.objects.create(customer_name=customer_name, phone=phone)

@sync_to_async
def create_order_item(order, product, quantity):
    return OrderItem.objects.create(order=order, product=product, quantity=quantity)

# Временное решение: храним корзину в памяти с улучшенной логикой
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

def remove_from_cart_db(user_id, product_id, quantity=1):
    """Удалить товар из корзины"""
    if user_id not in user_carts or product_id not in user_carts[user_id]:
        return False
    
    user_carts[user_id][product_id] -= quantity
    if user_carts[user_id][product_id] <= 0:
        del user_carts[user_id][product_id]
    
    return True

def clear_cart_db(user_id):
    """Очистить корзину пользователя"""
    if user_id in user_carts:
        user_carts[user_id] = {}
    return True

# Инициализация бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8268278368:AAHYyO96qA5rimH9C2HKWmTAaeMUD9pi7dQ')

if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    print("❌ Ошибка: Токен телеграм-бота не установлен!")
    print("📝 Для настройки токена:")
    print("1. Создайте файл .env в корневой директории проекта")
    print("2. Добавьте строку: TELEGRAM_BOT_TOKEN=your_actual_token_here")
    print("3. Получите токен у @BotFather в Telegram")
    print("4. Перезапустите бота")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = """
☕ Добро пожаловать в Sofia Coffee Bot!

Доступные команды:
/menu - Посмотреть меню
/cart - Посмотреть корзину
/order - Оформить заказ
/help - Помощь

Выберите действие:
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Меню", callback_data="show_menu")],
        [InlineKeyboardButton(text="🛒 Корзина", callback_data="show_cart")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])
    
    await message.answer(welcome_text, reply_markup=keyboard)

@dp.message(Command("menu"))
async def menu_command(message: types.Message):
    """Показать меню товаров"""
    await show_menu(message)

@dp.message(Command("cart"))
async def cart_command(message: types.Message):
    """Показать корзину"""
    await show_cart(message)

@dp.message(Command("order"))
async def order_command(message: types.Message):
    """Оформить заказ"""
    await create_order(message)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Показать помощь"""
    help_text = """
📖 Помощь по использованию бота:

/menu - Посмотреть все доступные товары
/cart - Посмотреть товары в корзине
/order - Оформить заказ из корзины
/test - Тестирование корзины
/clear - Очистить все корзины (для тестирования)
/help - Показать эту справку

Для добавления товара в корзину используйте кнопки в меню.
    """
    await message.answer(help_text)

@dp.message(Command("test"))
async def test_command(message: types.Message):
    """Тестирование корзины"""
    user_id = message.from_user.id
    
    # Добавляем тестовый товар
    add_to_cart_db(user_id, 1, 1)
    
    # Получаем товары из корзины
    cart_items = get_user_cart_items(user_id)
    
    test_text = f"""
🧪 <b>Тест корзины</b>

👤 Пользователь: {user_id}
👤 Имя: {message.from_user.first_name}
👤 Username: @{message.from_user.username or 'нет'}
📦 Товаров в корзине: {len(cart_items)}
📋 Детали: {cart_items}

🔍 Полная корзина: {user_carts.get(user_id, {})}
🔍 Все корзины: {user_carts}
    """
    
    await message.answer(test_text, parse_mode="HTML")

@dp.message(Command("clear"))
async def clear_command(message: types.Message):
    """Очистить все корзины (для тестирования)"""
    global user_carts
    user_carts = {}
    await message.answer("🗑 Все корзины очищены!")

async def show_menu(message: types.Message):
    """Показать меню товаров по категориям"""
    categories = await get_all_categories()
    
    if not categories:
        await message.answer("😔 К сожалению, категории временно недоступны.")
        return
    
    text = "📋 <b>Выберите категорию:</b>\n\n"
    keyboard_buttons = []
    
    for category in categories:
        # Добавляем эмодзи в зависимости от категории
        emoji = "☕" if "кофе" in category.name.lower() else "🍰" if "десерт" in category.name.lower() else "🥤"
        text += f"{emoji} <b>{category.name}</b>\n"
        
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"{emoji} {category.name}",
                callback_data=f"category_{category.id}"
            )
        ])
    
    keyboard_buttons.append([InlineKeyboardButton(text="🛒 Корзина", callback_data="show_cart")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

async def show_category_products(message: types.Message, category_id: int, page: int = 0, edit_message: types.Message = None):
    """Показать товары конкретной категории с пагинацией"""
    products = await get_products_by_category(category_id)
    
    if not products:
        if edit_message:
            await edit_message.edit_text("😔 В этой категории пока нет товаров.")
        else:
            await message.answer("😔 В этой категории пока нет товаров.")
        return
    
    # Получаем информацию о категории для эмодзи
    categories = await get_all_categories()
    category = next((cat for cat in categories if cat.id == category_id), None)
    category_emoji = "☕" if category and "кофе" in category.name.lower() else "🍰" if category and "десерт" in category.name.lower() else "🥤"
    
    # Проверяем корректность страницы
    if page < 0 or page >= len(products):
        page = 0
    
    product = products[page]
    
    product_text = f"{category_emoji} <b>{category.name if category else 'Товары'}</b>\n\n"
    product_text += f"<b>{product.name}</b>\n"
    product_text += f"💰 Цена: {product.price} ₽\n"
    if product.description:
        product_text += f"📝 {product.description}\n"
    product_text += f"\n📄 Страница {page + 1} из {len(products)}"
    
    keyboard_buttons = [
        [InlineKeyboardButton(
            text=f"➕ Добавить в корзину - {product.price} ₽",
            callback_data=f"add_to_cart_{product.id}"
        )]
    ]
    
    # Кнопки навигации по страницам
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{category_id}_{page-1}"))
    if page < len(products) - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{category_id}_{page+1}"))
    
    if nav_buttons:
        keyboard_buttons.append(nav_buttons)
    
    # Кнопки общего меню
    keyboard_buttons.append([InlineKeyboardButton(text="📋 Назад к категориям", callback_data="show_menu")])
    keyboard_buttons.append([InlineKeyboardButton(text="🛒 Корзина", callback_data="show_cart")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    # Проверяем наличие изображения
    if product.image and product.image.path and os.path.exists(product.image.path):
        try:
            photo = FSInputFile(product.image.path)
            if edit_message:
                try:
                    await edit_message.edit_media(
                        media=types.InputMediaPhoto(
                            media=photo,
                            caption=product_text,
                            parse_mode="HTML"
                        ),
                        reply_markup=keyboard
                    )
                except Exception as e:
                    print(f"Ошибка редактирования фото: {e}")
                    await edit_message.edit_text(product_text, reply_markup=keyboard, parse_mode="HTML")
            else:
                await message.answer_photo(
                    photo=photo,
                    caption=product_text,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
        except Exception as e:
            print(f"Ошибка отправки изображения: {e}")
            if edit_message:
                await edit_message.edit_text(product_text, reply_markup=keyboard, parse_mode="HTML")
            else:
                await message.answer(product_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        if edit_message:
            await edit_message.edit_text(product_text, reply_markup=keyboard, parse_mode="HTML")
        else:
            await message.answer(product_text, reply_markup=keyboard, parse_mode="HTML")

async def show_cart(message: types.Message, page: int = 0, edit_message: types.Message = None):
    """Показать корзину пользователя с пагинацией"""
    user_id = message.from_user.id
    
    cart_items = get_user_cart_items(user_id)
    print(f"DEBUG: Показ корзины для пользователя {user_id}")
    print(f"DEBUG: Товары в корзине: {cart_items}")
    print(f"DEBUG: Полная корзина пользователя: {user_carts.get(user_id, {})}")
    
    if not cart_items:
        if edit_message:
            await edit_message.edit_text("🛒 Ваша корзина пуста.\n\nИспользуйте /menu чтобы добавить товары.")
        else:
            await message.answer("🛒 Ваша корзина пуста.\n\nИспользуйте /menu чтобы добавить товары.")
        return
    
    # Проверяем корректность страницы
    if page < 0 or page >= len(cart_items):
        page = 0
    
    cart_item = cart_items[page]
    product_id = cart_item['product_id']
    quantity = cart_item['quantity']
    
    # Загружаем информацию о товаре
    product = await get_product_by_id(product_id)
    if not product:
        await message.answer("❌ Товар не найден!")
        return
    
    subtotal = product.price * quantity
    
    # Подсчитываем общую сумму
    total = 0
    for item in cart_items:
        item_product = await get_product_by_id(item['product_id'])
        if item_product:
            total += item_product.price * item['quantity']
    
    text = "🛒 <b>Ваша корзина</b>\n\n"
    text += f"<b>{product.name}</b>\n"
    text += f"📦 Количество: {quantity}\n"
    text += f"💰 Цена за штуку: {product.price} ₽\n"
    text += f"💰 Сумма: {subtotal} ₽\n\n"
    text += f"📄 Товар {page + 1} из {len(cart_items)}\n"
    text += f"💳 <b>Общий итог: {total} ₽</b>"
    
    keyboard_buttons = [
        [InlineKeyboardButton(text=f"➖ Убрать", callback_data=f"remove_from_cart_{product.id}"),
         InlineKeyboardButton(text=f"➕ Добавить", callback_data=f"add_to_cart_{product.id}")]
    ]
    
    # Кнопки навигации по товарам в корзине
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"cart_page_{page-1}"))
    if page < len(cart_items) - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"cart_page_{page+1}"))
    
    if nav_buttons:
        keyboard_buttons.append(nav_buttons)
    
    # Кнопки общего меню
    keyboard_buttons.append([InlineKeyboardButton(text="📋 Меню", callback_data="show_menu")])
    keyboard_buttons.append([InlineKeyboardButton(text="✅ Оформить заказ", callback_data="create_order")])
    keyboard_buttons.append([InlineKeyboardButton(text="🗑 Очистить корзину", callback_data="clear_cart")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    if edit_message:
        try:
            await edit_message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка редактирования сообщения: {e}")
            await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

async def create_order(message: types.Message):
    """Создать заказ"""
    user_id = message.from_user.id
    
    cart_items = get_user_cart_items(user_id)
    print(f"DEBUG: Создание заказа для пользователя {user_id}")
    print(f"DEBUG: Товары в корзине: {cart_items}")
    
    if not cart_items:
        await message.answer("🛒 Ваша корзина пуста. Добавьте товары из меню.")
        return
    
    # Создаем заказ
    order = await create_order_db(
        customer_name=f"Telegram User {message.from_user.first_name}",
        phone=f"@{message.from_user.username}" if message.from_user.username else "No username"
    )
    print(f"DEBUG: Создан заказ #{order.id}")
    
    # Добавляем товары в заказ
    for cart_item in cart_items:
        product = await get_product_by_id(cart_item['product_id'])
        if product:
            await create_order_item(order, product, cart_item['quantity'])
            print(f"DEBUG: Добавлен товар {product.name} в заказ #{order.id}")
    
    # Очищаем корзину
    clear_cart_db(user_id)
    print(f"DEBUG: Корзина пользователя {user_id} очищена")
    
    await message.answer(
        f"✅ <b>Заказ #{order.id} успешно оформлен!</b>\n\n"
        f"📞 Мы свяжемся с вами для подтверждения заказа.\n"
        f"💰 Сумма заказа будет рассчитана при подтверждении.",
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart_callback(callback: types.CallbackQuery):
    """Добавить товар в корзину"""
    product_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    
    product = await get_product_by_id(product_id)
    if product:
        add_to_cart_db(user_id, product_id, 1)
        print(f"DEBUG: Добавлен товар {product.name} (ID: {product_id}) для пользователя {user_id}")
        print(f"DEBUG: Текущая корзина пользователя {user_id}: {user_carts.get(user_id, {})}")
        await callback.answer(f"✅ {product.name} добавлен в корзину!")
    else:
        await callback.answer("❌ Товар не найден!")

@dp.callback_query(F.data.startswith("remove_from_cart_"))
async def remove_from_cart_callback(callback: types.CallbackQuery):
    """Удалить товар из корзины"""
    product_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    
    product = await get_product_by_id(product_id)
    if product:
        success = remove_from_cart_db(user_id, product_id, 1)
        if success:
            await callback.answer(f"➖ {product.name} удален из корзины!")
        else:
            await callback.answer("❌ Товар не найден в корзине!")
    else:
        await callback.answer("❌ Товар не найден!")

@dp.callback_query(F.data == "show_menu")
async def show_menu_callback(callback: types.CallbackQuery):
    """Показать меню через callback"""
    await show_menu(callback.message)
    await callback.answer()

@dp.callback_query(F.data.startswith("category_"))
async def category_callback(callback: types.CallbackQuery):
    """Показать товары категории"""
    category_id = int(callback.data.split("_")[-1])
    await show_category_products(callback.message, category_id, 0)
    await callback.answer()

@dp.callback_query(F.data.startswith("page_"))
async def page_callback(callback: types.CallbackQuery):
    """Обработчик пагинации"""
    try:
        parts = callback.data.split("_")
        category_id = int(parts[1])
        page = int(parts[2])
        await show_category_products(callback.message, category_id, page, callback.message)
        await callback.answer()
    except (ValueError, IndexError):
        await callback.answer("❌ Ошибка навигации!")

@dp.callback_query(F.data == "show_cart")
async def show_cart_callback(callback: types.CallbackQuery):
    """Показать корзину через callback"""
    await show_cart(callback.message, 0)
    await callback.answer()

@dp.callback_query(F.data.startswith("cart_page_"))
async def cart_page_callback(callback: types.CallbackQuery):
    """Обработчик пагинации корзины"""
    try:
        page = int(callback.data.split("_")[-1])
        await show_cart(callback.message, page, callback.message)
        await callback.answer()
    except (ValueError, IndexError):
        await callback.answer("❌ Ошибка навигации!")

@dp.callback_query(F.data == "create_order")
async def create_order_callback(callback: types.CallbackQuery):
    """Создать заказ через callback"""
    await create_order(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "clear_cart")
async def clear_cart_callback(callback: types.CallbackQuery):
    """Очистить корзину"""
    user_id = callback.from_user.id
    clear_cart_db(user_id)
    await callback.answer("🗑 Корзина очищена!")
    await show_cart(callback.message, 0)

@dp.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    """Показать помощь через callback"""
    await help_command(callback.message)
    await callback.answer()

async def main():
    """Запуск бота"""
    print("🤖 Запуск Sofia Coffee Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
