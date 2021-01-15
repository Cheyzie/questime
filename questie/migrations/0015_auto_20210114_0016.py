# Generated by Django 3.1.4 on 2021-01-13 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questie', '0014_auto_20210114_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dude',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$v7rcGgr0wv57$aNSINGM/0WZU1wMOdDIubiJyP/l4WTd7mtfwB2KxhSQ=', max_length=16),
        ),
        migrations.AlterField(
            model_name='image',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$7I8L2n6baVAY$enD2Gapq3wm7Obyu/u/LK7ISiEAxJwLzU31TFzuqVf0=', max_length=16),
        ),
        migrations.AlterField(
            model_name='result',
            name='quiz',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='questie.quiz'),
        ),
    ]