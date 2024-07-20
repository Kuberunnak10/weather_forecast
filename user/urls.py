from django.urls import path

from user.views import register

urlpatterns = [
    path('registration/', register, name='register'),
]