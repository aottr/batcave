from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.urls import reverse
from urllib.parse import urlencode
from storefront.models import Product, CartItem, ProductConfiguration, ProductSize, ProductColor, ProductFirmness
from storefront.forms import ProductConfiguratorForm, ProductConfigurationForm


def extract_choices(queryset):
    choices = []
    if queryset.exists():
        for entry in queryset.iterator():
            choices.append((entry.id, entry.__str__()))
    return choices


class CategoryView(ListView):
    model = Product
    paginate_by = 20


class ProductView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        size_choices = extract_choices(ProductSize.objects.filter(product=self.object))
        color_choices = extract_choices(ProductColor.objects.filter(product=self.object))
        firmness_choices = extract_choices(ProductFirmness.objects.filter(product=self.object))
        context['form'] = ProductConfigurationForm(size_choices=size_choices, color_choices=color_choices,
                                                   firmness_choices=firmness_choices)
        return context

    def post(self, request, slug, **kwargs):
        form = ProductConfigurationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data.get('size'))
            return redirect('cart')

            # if a GET (or any other method) we'll create a blank form

        else:
            form = ProductConfigurationForm()

        return render(request, 'storefront/product_detail.html', {"form": form})


class CartView(ListView):
    model = CartItem
    template_name = 'storefront/cart.html'


def empty_cart(request):
    request.user.cart.items.clear()
    request.user.cart.save()
    return redirect('cart')


def add_to_cart(request, slug):
    # TODO Error handling

    cart = request.user.cart

    if request.method != 'POST':
        return redirect('product-detail', slug=slug)

    product = Product.objects.get(slug=slug)

    config = ProductConfiguration.objects.create(product=product)
    cart.items.add(CartItem.objects.create(item=config))
    cart.total += config.product.base_price

    if config.size:
        cart.total += config.size.markup
    if config.color:
        cart.total += config.color.markup
    if config.firmness:
        cart.total += config.firmness.markup

    cart.save()

    return redirect('product-detail', slug=slug)
