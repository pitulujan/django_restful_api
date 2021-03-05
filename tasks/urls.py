from django.urls import path
from . import views

urlpatterns = [
    path('get_tasks/<str:task_id>/', views.GetTasks.as_view(), name='get_tasks'),
    path('get_tasks/', views.GetTasks.as_view(), name='get_tasks'),
]