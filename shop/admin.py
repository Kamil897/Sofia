from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, Promo, News, Review, Recommendation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}  # автоматическая генерация slug
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)  # ✅ фильтрация по категориям
    search_fields = ("name",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "phone", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity")
    list_filter = ("product", "order")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "added_at")
    list_filter = ("product", "added_at")
    search_fields = ("product__name",)


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "discount", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("name", "description")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published_at")
    list_filter = ("published_at",)
    search_fields = ("title", "text")
    ordering = ("-published_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("customer_name", "text")
    ordering = ("-created_at",)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "recommended_product")
    list_filter = ("product", "recommended_product")
    search_fields = ("product__name", "recommended_product__name")
