# Generated by Django 3.0.1 on 2019-12-24 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinaceNote', '0002_auto_20191224_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='user_city',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='upload',
            name='user_hobby',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='upload',
            name='user_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='upload',
            name='user_pass',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='upload',
            name='user_sex',
            field=models.CharField(max_length=20),
        ),
    ]
