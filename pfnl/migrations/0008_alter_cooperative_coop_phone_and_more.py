# Generated by Django 5.0.3 on 2024-04-05 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfnl', '0007_remove_product_type_product_prod_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperative',
            name='coop_phone',
            field=models.CharField(max_length=14, unique=True, verbose_name='Numéro de téléphone'),
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_1',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem')], default='None', max_length=10, verbose_name='Produit offert 1'),
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_2',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem')], default='None', max_length=10, verbose_name='Produit offert 2'),
        ),
        migrations.AlterField(
            model_name='cooperative',
            name='offered_product_3',
            field=models.CharField(choices=[('None', ''), ('AK', 'Amande de karité'), ('BK', 'Beurre de karité'), ('SO', 'Soumabala'), ('BS', 'Biscuit de pain de singe'), ('JS', 'Jus de pain de singe'), ('SN', 'Savon de neem'), ('HN', 'Huile de neem')], default='None', max_length=10, verbose_name='Produit offert 1'),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_phone',
            field=models.CharField(max_length=14, unique=True, verbose_name='Numéro de téléphone'),
        ),
    ]
