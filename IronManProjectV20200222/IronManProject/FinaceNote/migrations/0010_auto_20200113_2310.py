# Generated by Django 3.0.1 on 2020-01-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinaceNote', '0009_upload_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='user_filename',
            field=models.CharField(max_length=5000),
        ),
    ]
