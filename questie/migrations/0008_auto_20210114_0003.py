# Generated by Django 3.1.4 on 2021-01-13 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questie', '0007_auto_20210114_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dude',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$4kSenvY8qLGy$ateyEotH5F6ItQE2IVg4YVHahhpX0qcP+7+yYMYcYwQ=', max_length=16),
        ),
        migrations.AlterField(
            model_name='image',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$lYwb92W9dSYX$rM7Dfmhwy0xTwsRsyBA97IUuwSskgxK25IFjH8JtUB4=', max_length=16),
        ),
    ]