# Generated by Django 3.1.4 on 2021-01-13 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questie', '0008_auto_20210114_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dude',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$0wm6bQgBPPq4$SLOzo0dEPhrhIbKnJ6/daZ4nX8WyIdC3t52MxVYfkXY=', max_length=16),
        ),
        migrations.AlterField(
            model_name='image',
            name='editing_key',
            field=models.CharField(blank=True, default='pbkdf2_sha256$216000$EIXPz8IEbMmm$M6XI7d3SBcCDn5ppsiCzNYKgtDfYT5nYcdA78W6uNAo=', max_length=16),
        ),
    ]
