# Generated by Django 2.2 on 2020-06-09 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20200608_2327'),
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
