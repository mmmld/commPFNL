# Generated by Django 5.0.3 on 2024-04-17 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfnl', '0011_member_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='telegram_id',
            field=models.IntegerField(verbose_name='ID telegram'),
        ),
    ]
