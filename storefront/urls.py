from django.urls import path

from .views import ProductView, CategoryView, CartView, empty_cart, product_detail

urlpatterns = [
    path('', CategoryView.as_view(), name='category-detail'),
    path('cart', CartView.as_view(), name='cart'),
    path('cart/empty', empty_cart, name='empty-cart'),
    path('pp/<slug:slug>', product_detail, name='product-detail'),
]
