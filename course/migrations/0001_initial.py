# Generated by Django 3.2.13 on 2022-04-19 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('descripation', models.CharField(max_length=300, null=True)),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('thumbnail', models.ImageField(upload_to='file/thumbnail')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('resource', models.FileField(upload_to='file/resource')),
                ('length', models.IntegerField()),
            ],
        ),
    ]
