from django.urls import path
from . import views

urlpatterns = [
    path('get_token', views.GetToken.as_view(), name='get_token'),
]