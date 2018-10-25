# Generated by Django 2.1.2 on 2018-10-23 23:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0006_remove_cart_category'),
        ('cart', '0002_auto_20181018_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestCart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular product across whole system', primary_key=True, serialize=False)),
                ('next_ship', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('b', 'Browsing'), ('o', 'ORDER'), ('a', 'a'), ('c', 'Cancelled')], default='t', help_text='Product availability', max_length=1)),
                ('cartItems', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.CartItem')),
            ],
            options={
                'ordering': ['next_ship'],
            },
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
