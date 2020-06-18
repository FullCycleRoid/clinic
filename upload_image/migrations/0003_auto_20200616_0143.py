# Generated by Django 3.0.6 on 2020-06-15 22:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('upload_image', '0002_image_users_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadimage',
            name='created',
            field=models.DateField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='image',
            field=models.ImageField(default=datetime.datetime(2020, 6, 15, 22, 43, 24, 58936, tzinfo=utc), upload_to='images/%Y/%m/%d/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='title',
            field=models.CharField(default=datetime.datetime(2020, 6, 16, 1, 43, 34, 658881), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='url',
            field=models.URLField(default=datetime.datetime.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='images_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadimage',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='images_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]