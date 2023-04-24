from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse
from urllib.parse import urlencode
from storefront.models import Product, CartItem


class CategoryView(ListView):
    model = Product
    paginate_by = 20


class ProductView(DetailView):
    model = Product


def add_to_cart(request, slug):
    # TODO Error handling
    product = Product.objects.get(slug=slug)
    request.user.cart.items.add(CartItem.objects.create(item=product))
    request.user.cart.total += product.base_price
    request.user.cart.save()

    return redirect('product-detail', slug=slug)
