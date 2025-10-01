from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Order, OrderItem, Category, Cart, Promo, News, Review, Recommendation
from .forms import OrderForm

def index(request):
    return render(request, "shop/index.html")

def menu(request):
    products = Product.objects.all()
    return render(request, "shop/menu.html", {"products": products})

def cart(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        items.append({"product": product, "quantity": qty, "subtotal": product.price * qty})
        total += product.price * qty
    return render(request, "shop/cart.html", {"items": items, "total": total})

def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    return redirect("cart")

def order(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("menu")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for product_id, qty in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(order=order, product=product, quantity=qty)
            request.session["cart"] = {}
            return render(request, "shop/order.html", {"order": order, "success": True})
    else:
        form = OrderForm()

    return render(request, "shop/order.html", {"form": form})

def menu(request):
    category_id = request.GET.get("category")  # берём выбранную категорию из query-параметра
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    return render(request, "shop/menu.html", {
        "products": products,
        "categories": categories,
        "selected_category": int(category_id) if category_id else None,
    })


# Новые представления для добавленных моделей
class CartListView(ListView):
    model = Cart
    template_name = 'shop/cart_list.html'
    context_object_name = 'cart_items'
    paginate_by = 10


class PromoListView(ListView):
    model = Promo
    template_name = 'shop/promo_list.html'
    context_object_name = 'promos'
    paginate_by = 10

    def get_queryset(self):
        from django.utils import timezone
        return Promo.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).order_by('-start_date')


class PromoDetailView(DetailView):
    model = Promo
    template_name = 'shop/promo_detail.html'
    context_object_name = 'promo'


class NewsListView(ListView):
    model = News
    template_name = 'shop/news_list.html'
    context_object_name = 'news'
    paginate_by = 10


class NewsDetailView(DetailView):
    model = News
    template_name = 'shop/news_detail.html'
    context_object_name = 'news'


class ReviewListView(ListView):
    model = Review
    template_name = 'shop/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'shop/review_detail.html'
    context_object_name = 'review'


class RecommendationListView(ListView):
    model = Recommendation
    template_name = 'shop/recommendation_list.html'
    context_object_name = 'recommendations'
    paginate_by = 10

    def get_queryset(self):
        product_id = self.request.GET.get('product_id')
        if product_id:
            return Recommendation.objects.filter(product_id=product_id)
        return Recommendation.objects.all()

