from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.create_tool_date, name='create_tool_date'),
    path('<int:pk>', views.tool_date_details, name='tool_date_details')
]
