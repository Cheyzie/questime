# Generated by Django 3.1.4 on 2021-01-13 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questie', '0009_auto_20210114_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dude',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$GDwnXbY3HiQ5$R3KjZGArOc/ItAPhMQUoceFjYRJWzBpe81pXAEYdlRY=', max_length=16),
        ),
        migrations.AlterField(
            model_name='image',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$pIWxrmPAW8jv$gIbjRgxu3MqWPPPQIhNFez+jmR81on/GicX9yrzuapU=', max_length=16),
        ),
    ]
