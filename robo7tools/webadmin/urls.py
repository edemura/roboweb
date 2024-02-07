from django.urls import path
from . import views

urlpatterns = [
    path('configs/', views.configs, name='configs'),
    path('poll/', views.poll, name='poll'),
    path('stop/', views.stop, name='stop'),
    path('dir/', views.dir, name='dir'),
    path('task/', views.task, name="task"),
    path('task/<int:task_id>/', views.task_id, name="task_id"),
    path('<int:task_id>/run', views.task_run, name="task_run"),
    path('<int:task_id>/stop', views.task_stop, name="task_stop"),

]