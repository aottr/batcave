from django.contrib import admin
from storefront.models import Product, Category, ProductSize, ProductColor, ProductConfiguration, ProductFirmness, ProductImage, Cart


admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(ProductConfiguration)


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    classes = ('collapse',)


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    classes = ('collapse',)


class ProductFirmnessInline(admin.TabularInline):
    model = ProductFirmness
    extra = 1
    classes = ('collapse',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    classes = ('collapse',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline, ProductColorInline, ProductFirmnessInline, ProductImageInline]
