# Generated by Django 3.2.12 on 2022-04-21 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_videomodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemodel',
            name='slug',
            field=models.CharField(default='char', max_length=350),
        ),
    ]