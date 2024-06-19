# Generated by Django 5.0.3 on 2024-05-13 12:22

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfnl', '0014_alter_cooperative_coop_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtemisiaSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True, verbose_name='Numéro de téléphone')),
                ('telegram_id', models.IntegerField(default=0, verbose_name='ID telegram')),
            ],
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_3',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem'), ('PM', 'Poudre de moringa'), ('PB', 'Poudre de baobab'), ('TS', 'Tisane'), ('ML', 'Miel'), ('FB', 'Feuilles de balanites'), ('JB', 'Jus de balanites'), ('ZM', 'Zamenin')], default='None', max_length=10, verbose_name='Produit offert 3'),
        ),
        migrations.CreateModel(
            name='ArtemisiaProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_type', models.CharField(choices=[('None', ''), ('TA', 'Tisane'), ('PA', 'Pied'), ('SA', 'Graine')], default='None', max_length=10, verbose_name='Type de produit')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantité')),
                ('price', models.IntegerField(default=0, verbose_name='Prix')),
                ('last_modified', models.DateField(auto_now_add=True, verbose_name='Dernière modification')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfnl.artemisiaseller')),
            ],
        ),
    ]
