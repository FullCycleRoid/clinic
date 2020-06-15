from django.contrib import admin
from .models import UploadImage


@admin.register(UploadImage)
class ImageAdmin(admin.ModelAdmin):
 list_display = ['title', 'slug', 'image', 'created']
 list_filter = ['created']