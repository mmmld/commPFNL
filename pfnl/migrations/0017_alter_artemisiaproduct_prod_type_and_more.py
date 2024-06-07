# Generated by Django 5.0.3 on 2024-06-07 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pfnl", "0016_merge_20240607_0811"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artemisiaproduct",
            name="prod_type",
            field=models.CharField(
                choices=[
                    ("None", ""),
                    ("TA", "Tisane d'artemisia"),
                    ("PA", "Pied d'artemisia"),
                    ("SA", "Graine d'artemisia"),
                ],
                default="None",
                max_length=10,
                verbose_name="Type de produit",
            ),
        ),
        migrations.AlterField(
            model_name="cooperative",
            name="offered_product_1",
            field=models.CharField(
                choices=[
                    ("None", ""),
                    ("AK", "Amande de karité"),
                    ("BK", "Beurre de karité"),
                    ("SO", "Soumbala"),
                    ("BS", "Biscuit de pain de singe"),
                    ("JS", "Jus de pain de singe"),
                    ("SN", "Savon de neem"),
                    ("HN", "Huile de neem"),
                    ("PM", "Poudre de moringa"),
                    ("PB", "Poudre de baobab"),
                    ("TS", "Tisane"),
                    ("ML", "Miel"),
                    ("FB", "Feuilles de balanites"),
                    ("JB", "Jus de balanites"),
                    ("ZM", "Zamenin"),
                ],
                default="None",
                max_length=10,
                verbose_name="Produit offert 1",
            ),
        ),
        migrations.AlterField(
            model_name="cooperative",
            name="offered_product_2",
            field=models.CharField(
                choices=[
                    ("None", ""),
                    ("AK", "Amande de karité"),
                    ("BK", "Beurre de karité"),
                    ("SO", "Soumbala"),
                    ("BS", "Biscuit de pain de singe"),
                    ("JS", "Jus de pain de singe"),
                    ("SN", "Savon de neem"),
                    ("HN", "Huile de neem"),
                    ("PM", "Poudre de moringa"),
                    ("PB", "Poudre de baobab"),
                    ("TS", "Tisane"),
                    ("ML", "Miel"),
                    ("FB", "Feuilles de balanites"),
                    ("JB", "Jus de balanites"),
                    ("ZM", "Zamenin"),
                ],
                default="None",
                max_length=10,
                verbose_name="Produit offert 2",
            ),
        ),
        migrations.AlterField(
            model_name="cooperative",
            name="offered_product_3",
            field=models.CharField(
                choices=[
                    ("None", ""),
                    ("AK", "Amande de karité"),
                    ("BK", "Beurre de karité"),
                    ("SO", "Soumbala"),
                    ("BS", "Biscuit de pain de singe"),
                    ("JS", "Jus de pain de singe"),
                    ("SN", "Savon de neem"),
                    ("HN", "Huile de neem"),
                    ("PM", "Poudre de moringa"),
                    ("PB", "Poudre de baobab"),
                    ("TS", "Tisane"),
                    ("ML", "Miel"),
                    ("FB", "Feuilles de balanites"),
                    ("JB", "Jus de balanites"),
                    ("ZM", "Zamenin"),
                ],
                default="None",
                max_length=10,
                verbose_name="Produit offert 3",
            ),
        ),
    ]
