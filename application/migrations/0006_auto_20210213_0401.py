# Generated by Django 3.1.4 on 2021-02-12 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completeorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.userinfo'),
        ),
    ]
