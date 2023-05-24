from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, ListView
from storefront.models import Product, CartItem, ProductConfiguration, ProductSize, ProductColor, ProductFirmness, ProductImage
from storefront.forms import ProductConfigurationForm
from storefront.utils import calculate_stock


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
    product_images = ProductImage.objects.filter(product=product)

    size_choices = extract_choices(ProductSize.objects.filter(product=product))
    color_choices = extract_choices(ProductColor.objects.filter(product=product))
    firmness_choices = extract_choices(ProductFirmness.objects.filter(product=product))

    if request.method == 'POST':
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return redirect('login')

        form = ProductConfigurationForm(request.POST, user=request.user, product=product, size_choices=size_choices,
                                        color_choices=color_choices,
                                        firmness_choices=firmness_choices)
        if form.is_valid():

            cart = request.user.cart
            config = ProductConfiguration(
                product=product,
                color=form.cleaned_data.get('color'),
                firmness=form.cleaned_data.get('firmness'),
                size=form.cleaned_data.get('size'),
                note=form.cleaned_data.get('note')
            )
            new_cart_item = CartItem(cart=cart, item=config, amount=form.cleaned_data.get('amount'))

            other_cart_items = CartItem.objects.filter(cart=cart)
            create = True
            for cart_item in other_cart_items.iterator():
                if cart_item.item.compare_with(config):
                    create = False
                    cart_item.amount += new_cart_item.amount
                    cart_item.save()

            if create:
                config.save()
                new_cart_item.save()

            calculate_stock(new_cart_item)

    else:
        form = ProductConfigurationForm(user=request.user, product=product, size_choices=size_choices,
                                        color_choices=color_choices,
                                        firmness_choices=firmness_choices)
    return render(request, 'storefront/product_detail.html', {"form": form, 'object': product, 'images': product_images})


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

    @login_required
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
        calculate_stock(item, False)
        item.delete()

    return redirect('cart')
