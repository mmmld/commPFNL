# Generated by Django 5.0.3 on 2024-04-23 14:14

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfnl', '0013_alter_member_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperative',
            name='coop_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True, verbose_name='Numéro de téléphone'),
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_1',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem'), ('PM', 'Poudre de moringa'), ('PB', 'Poudre de baobab'), ('TS', 'Tisane'), ('ML', 'Miel'), ('FB', 'Feuilles de balanites'), ('JB', 'Jus de balanites'), ('ZM', 'Zamenin')], default='None', max_length=10, verbose_name='Produit offert 1'),
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_2',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem'), ('PM', 'Poudre de moringa'), ('PB', 'Poudre de baobab'), ('TS', 'Tisane'), ('ML', 'Miel'), ('FB', 'Feuilles de balanites'), ('JB', 'Jus de balanites'), ('ZM', 'Zamenin')], default='None', max_length=10, verbose_name='Produit offert 2'),
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_3',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem'), ('PM', 'Poudre de moringa'), ('PB', 'Poudre de baobab'), ('TS', 'Tisane'), ('ML', 'Miel'), ('FB', 'Feuilles de balanites'), ('JB', 'Jus de balanites'), ('ZM', 'Zamenin')], default='None', max_length=10, verbose_name='Produit offert 1'),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True, verbose_name='Numéro de téléphone'),
        ),
    ]
