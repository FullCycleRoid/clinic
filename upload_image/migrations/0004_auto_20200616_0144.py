# Generated by Django 3.0.6 on 2020-06-15 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_image', '0003_auto_20200616_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadimage',
            name='created',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
    ]
