from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('messages/', views.get_messages, name='get_messages'),
]
