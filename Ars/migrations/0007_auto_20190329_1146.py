# Generated by Django 2.1.7 on 2019-03-29 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ars', '0006_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qrcodemodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idNo', models.IntegerField()),
                ('qrImageName', models.CharField(max_length=250)),
                ('category', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='link',
            name='session',
        ),
        migrations.RemoveField(
            model_name='option',
            name='option_type',
        ),
        migrations.AddField(
            model_name='question',
            name='option_type',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='qr_link_name',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.DeleteModel(
            name='Link',
        ),
    ]
