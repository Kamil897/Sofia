from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("order/", views.order, name="order"),
    
    # Новые URL-маршруты
    path("cart-list/", views.CartListView.as_view(), name="cart_list"),
    path("promo/", views.PromoListView.as_view(), name="promo_list"),
    path("promo/<int:pk>/", views.PromoDetailView.as_view(), name="promo_detail"),
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/<int:pk>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("reviews/", views.ReviewListView.as_view(), name="review_list"),
    path("reviews/<int:pk>/", views.ReviewDetailView.as_view(), name="review_detail"),
    path("recommendations/", views.RecommendationListView.as_view(), name="recommendation_list"),
]
