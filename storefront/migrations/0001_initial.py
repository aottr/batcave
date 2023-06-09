# Generated by Django 4.2 on 2023-04-25 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('priority', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('priority', models.SmallIntegerField(default=0)),
                ('base_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, quality=-1, scale=None, size=[600, 600], upload_to='store/thumbnails/')),
                ('active', models.BooleanField(default=True)),
                ('stock', models.SmallIntegerField(default=0)),
                ('per_user_limit', models.SmallIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=120)),
                ('markup', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=120)),
                ('markup', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFirmness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firmness', models.CharField(max_length=120)),
                ('markup', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCustomField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('option', models.CharField(blank=True, max_length=500, null=True)),
                ('priority', models.SmallIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storefront.productcolor')),
                ('firmness', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storefront.productfirmness')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storefront.productsize')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.productconfiguration')),
            ],
        ),
    ]
