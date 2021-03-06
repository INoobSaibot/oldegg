# Generated by Django 2.1.2 on 2018-11-04 01:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20181030_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular product across whole system', primary_key=True, serialize=False)),
                ('cardNumber', models.IntegerField(help_text='Enter a fake card number', max_length=16, verbose_name='CardNumber')),
                ('cvv', models.IntegerField(help_text='max length = 4', max_length=4, verbose_name='cvv')),
            ],
        ),
    ]
