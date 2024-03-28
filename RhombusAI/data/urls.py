from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path

app_name = 'data'

urlpatterns = [
    path('upload/', views.upload_file, name='file_upload'),
]
