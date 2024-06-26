# Generated by Django 5.0.3 on 2024-04-03 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coop_name', models.CharField(max_length=50)),
                ('coop_phone', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_name', models.CharField(max_length=50)),
                ('member_phone', models.CharField(max_length=13)),
                ('coop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfnl.cooperative')),
            ],
        ),
        migrations.CreateModel(
            name='TypeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_product_name', models.CharField(max_length=50)),
                ('coop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfnl.cooperative')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfnl.member')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pfnl.typeproduct')),
            ],
        ),
    ]
