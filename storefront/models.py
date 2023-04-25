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
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    priority = models.SmallIntegerField(default=0)

    base_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='store/thumbnails/', blank=True)

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
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.color


class ProductFirmness(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    firmness = models.CharField(max_length=120)
    markup = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.firmness


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    size = models.CharField(max_length=120)
    markup = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.size


class ProductConfiguration(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    color = models.ForeignKey(ProductColor, null=True, blank=True, on_delete=models.CASCADE, )
    size = models.ForeignKey(ProductSize, null=True, blank=True, on_delete=models.CASCADE, )
    firmness = models.ForeignKey(ProductFirmness, null=True, blank=True, on_delete=models.CASCADE, )
    note = models.TextField(blank=True)


class CartItem(models.Model):
    item = models.ForeignKey(ProductConfiguration, on_delete=models.CASCADE, )
    amount = models.PositiveSmallIntegerField(default=1)


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, )
    items = models.ManyToManyField(CartItem, null=True, blank=True, )
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)


@receiver(post_save, sender=User)
def create_favorites(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)