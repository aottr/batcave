from django.urls import path

from .views import ProductView, CategoryView

urlpatterns = [
    path('', CategoryView.as_view(), name='category-detail'),
    path('pp/<slug:slug>', ProductView.as_view(), name='product-detail'),
]
