from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.student_create, name='student_create'),
    path('', views.student_list, name='student_list'),
]