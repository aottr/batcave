from django.db import models
from django_resized import ResizedImageField


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170)
    priority = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=170)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    priority = models.SmallIntegerField(default=0)

    base_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='store/thumbnails/', blank=True)

    def __str__(self):
        return self.name


class ProductCustomField(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    name = models.CharField(max_length=255)
    option = models.CharField(max_length=500, null=True, blank=True)
    priority = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name
