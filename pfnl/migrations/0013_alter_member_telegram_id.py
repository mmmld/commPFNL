# Generated by Django 5.0.3 on 2024-04-17 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfnl', '0012_alter_member_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='telegram_id',
            field=models.IntegerField(default=0, verbose_name='ID telegram'),
        ),
    ]
