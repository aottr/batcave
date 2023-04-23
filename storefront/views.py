from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from storefront.models import Product


class CategoryView(ListView):
    model = Product
    paginate_by = 20


class ProductView(DetailView):
    model = Product
