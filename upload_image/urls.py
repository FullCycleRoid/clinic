from django.urls import path
from .views import create_image

app_name = 'upload_image'

urlpatterns = [
    path('create_image/', create_image, name='create_image')
]