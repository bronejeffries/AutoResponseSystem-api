# Generated by Django 2.1.7 on 2019-02-26 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='status',
            field=models.CharField(default='running', max_length=25),
        ),
    ]
