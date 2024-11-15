from django.urls import path
from . import views

urlpatterns = [
    path('api/process-interval', views.process_interval, name='process_interval'),
    path('api/process-combine', views.process_combine, name='process_combine'),
]
