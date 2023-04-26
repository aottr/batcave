from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    priority = models.SmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT = 'PT'
    COLOR = 'CR'
    SIZE = 'SZ'

    STOCK_CHOICES = (
        (PRODUCT, 'Product Stock'),
        (COLOR, 'Color Stock'),
        (SIZE, 'Size Stock'),
    )

    class StockChoices(models.TextChoices):
        PRODUCT = 'PT', 'Product Stock'
        COLOR = 'CR', 'Color Stock'
        SIZE = 'SZ', 'Size Stock'

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    priority = models.SmallIntegerField(default=0)

    base_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='store/thumbnails/', blank=True)

    active = models.BooleanField(default=True)
    stock = models.SmallIntegerField(default=0)
    per_user_limit = models.SmallIntegerField(default=0)
    stock_selector = models.CharField(max_length=2, choices=StockChoices.choices, default=StockChoices.PRODUCT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductCustomField(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    name = models.CharField(max_length=255)
    option = models.CharField(max_length=500, null=True, blank=True)
    priority = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    color = models.CharField(max_length=120)
    markup = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    stock = models.SmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.color if self.markup == 0 else f"{self.color} (+${self.markup})"


class ProductFirmness(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    firmness = models.CharField(max_length=120)
    markup = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.firmness if self.markup == 0 else f"{self.firmness} (+${self.markup})"


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    size = models.CharField(max_length=120)
    markup = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    stock = models.SmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.size if self.markup == 0 else f"{self.size} (+${self.markup})"


class ProductConfiguration(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    color = models.ForeignKey(ProductColor, null=True, blank=True, on_delete=models.CASCADE, )
    size = models.ForeignKey(ProductSize, null=True, blank=True, on_delete=models.CASCADE, )
    firmness = models.ForeignKey(ProductFirmness, null=True, blank=True, on_delete=models.CASCADE, )
    note = models.TextField(blank=True)

    def compare_with(self, other_config):
        return (self.product == other_config.product and self.color == other_config.color
                and self.size == other_config.size and self.firmness == other_config.firmness
                and self.note == other_config.note)

    def calculate_total(self):
        total = self.product.base_price
        if self.size:
            total += self.size.markup
        if self.color:
            total += self.color.markup
        if self.firmness:
            total += self.firmness.markup

        return total


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, )

    def get_items(self):
        return CartItem.objects.filter(cart=self)

    def count_items(self):
        items = self.get_items()
        count = 0
        for item in items.iterator():
            count += item.amount
        return count

    def get_total(self):
        items = self.get_items()
        total = 0
        for item in items.iterator():
            total += item.item.calculate_total() * item.amount
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, )
    item = models.ForeignKey(ProductConfiguration, on_delete=models.CASCADE, )
    amount = models.PositiveSmallIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        return self.item.calculate_total() * self.amount
    # TODO add timer


@receiver(post_save, sender=User)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)


# @receiver(post_save, sender=CartItem)
# def check_cart_duplicates(sender, instance, created, **kwargs):
#     if created:
#         other_cart_items = CartItem.objects.filter(cart=instance.cart).exclude(item=instance)
#         for cart_item in other_cart_items.iterator():
#             if cart_item.item.compare_with(instance.item):
#                 cart_item.amount += instance.amount
#         Cart.objects.create(owner=instance)
