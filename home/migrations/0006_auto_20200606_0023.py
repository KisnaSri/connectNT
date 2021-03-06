# Generated by Django 2.2 on 2020-06-05 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20200605_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='image',
            field=models.ImageField(upload_to='adImages'),
        ),
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='authorImages/'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogPostImages/'),
        ),
        migrations.AlterField(
            model_name='postimages',
            name='image',
            field=models.ImageField(upload_to='postImages/'),
        ),
    ]
