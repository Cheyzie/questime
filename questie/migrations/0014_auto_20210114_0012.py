# Generated by Django 3.1.4 on 2021-01-13 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questie', '0013_auto_20210114_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dude',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$dl4UEEucUZmJ$hViUFFpj8JVH9h3S/ts5tNvijRYlsgwLtu68vmvV33c=', max_length=16),
        ),
        migrations.AlterField(
            model_name='image',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$kRulgGNDvSEE$cokWUp8KV/Wbxy3PhTnfvlKIU079gQM+UvlDbTG8LSs=', max_length=16),
        ),
    ]
