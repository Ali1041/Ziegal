# Generated by Django 3.1.4 on 2021-07-19 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0020_product_learn_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='learn_more',
            field=models.TextField(blank=True, null=True),
        ),
    ]