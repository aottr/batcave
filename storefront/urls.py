from django.urls import path

from .views import ProductView, CategoryView, add_to_cart, CartView, empty_cart

urlpatterns = [
    path('', CategoryView.as_view(), name='category-detail'),
    path('cart', CartView.as_view(), name='cart'),
    path('cart/empty', empty_cart, name='empty-cart'),
    path('pp/<slug:slug>', ProductView.as_view(), name='product-detail'),
    path('pp/<slug:slug>/add', add_to_cart, name='add-to-cart'),
]
