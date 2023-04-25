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


def product_detail(request, slug, **kwargs):
    product = Product.objects.get(slug=slug)

    size_choices = extract_choices(ProductSize.objects.filter(product=product))
    color_choices = extract_choices(ProductColor.objects.filter(product=product))
    firmness_choices = extract_choices(ProductFirmness.objects.filter(product=product))

    if request.method == 'POST':
        form = ProductConfigurationForm(request.POST, user=request.user, product=product, size_choices=size_choices,
                                        color_choices=color_choices,
                                        firmness_choices=firmness_choices)
        if form.is_valid():

            cart = request.user.cart
            config = ProductConfiguration.objects.create(
                product=product,
                color=form.cleaned_data.get('color'),
                firmness=form.cleaned_data.get('firmness'),
                size=form.cleaned_data.get('size'),
                note=form.cleaned_data.get('note')
            )
            CartItem.objects.create(cart=cart, item=config, amount=form.cleaned_data.get('amount'))
            product.stock -= form.cleaned_data.get('amount')
            product.save()

    else:
        form = ProductConfigurationForm(user=request.user, product=product, size_choices=size_choices,
                                        color_choices=color_choices,
                                        firmness_choices=firmness_choices)
    return render(request, 'storefront/product_detail.html', {"form": form, 'object': product})


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
        product = Product.objects.get(slug=slug)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data.get('size'))
            return redirect('cart')

        return render(request, 'storefront/product_detail.html', {"form": form, 'object': product})


class CartView(ListView):
    model = CartItem
    template_name = 'storefront/cart.html'


def empty_cart(request):

    items = CartItem.objects.filter(cart=request.user.cart)
    for item in items.iterator():
        item.item.product.stock += item.amount
        item.item.product.save()
        item.delete()

    return redirect('cart')
