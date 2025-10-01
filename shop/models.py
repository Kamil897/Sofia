from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категория")
    slug = models.SlugField(max_length=100, unique=True)  # для URL (например, /menu/coffee/)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Категория",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(
        max_length=20,
        choices=[("new", "Новый"), ("cooking", "Готовится"), ("done", "Готово")],
        default="new",
        verbose_name="Статус"
    )

    def __str__(self):
        return f"Заказ #{self.id} от {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Cart(models.Model):
    user_id = models.BigIntegerField(verbose_name="ID пользователя Telegram")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        unique_together = ['user_id', 'product']

    def __str__(self):
        return f"User {self.user_id}: {self.product.name} x {self.quantity}"


class Promo(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Скидка (%)")
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")

    class Meta:
        verbose_name = "Промо-акция"
        verbose_name_plural = "Промо-акции"

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Review(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.rating}/5"


class Recommendation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="recommendations", verbose_name="Товар")
    recommended_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="recommended_for", verbose_name="Рекомендуемый товар")

    class Meta:
        verbose_name = "Рекомендация"
        verbose_name_plural = "Рекомендации"
        unique_together = ['product', 'recommended_product']

    def __str__(self):
        return f"{self.product.name} → {self.recommended_product.name}"
