# Generated by Django 2.1.2 on 2018-11-15 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_paymentcard_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='orders',
            field=models.ManyToManyField(to='cart.TestCart'),
        ),
    ]