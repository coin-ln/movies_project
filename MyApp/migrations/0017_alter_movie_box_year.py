# Generated by Django 4.2.10 on 2024-05-08 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0016_movie_box'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie_box',
            name='year',
            field=models.PositiveIntegerField(verbose_name='年份'),
        ),
    ]