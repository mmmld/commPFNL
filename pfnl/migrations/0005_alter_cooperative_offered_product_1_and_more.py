# Generated by Django 5.0.3 on 2024-04-04 09:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfnl', '0004_alter_cooperative_offered_product_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_1',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem')], default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_2',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem')], default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_3',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem')], default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_modified',
            field=models.DateField(default=datetime.datetime(2024, 4, 4, 9, 45, 34, 358119, tzinfo=datetime.timezone.utc), verbose_name='Dernière modification'),
        ),
    ]
