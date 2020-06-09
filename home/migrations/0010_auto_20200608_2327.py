# Generated by Django 2.2 on 2020-06-08 17:42

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20200608_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='adImages'),
        ),
        migrations.AlterField(
            model_name='author',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='authorImages'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='blogpostImages'),
        ),
        migrations.AlterField(
            model_name='postimages',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='postImages'),
        ),
    ]