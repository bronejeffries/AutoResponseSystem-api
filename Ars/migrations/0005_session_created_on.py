# Generated by Django 2.1.7 on 2019-03-10 18:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Ars', '0004_auto_20190308_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
