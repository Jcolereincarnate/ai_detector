from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check/', views.plagiarism_check, name='plagiarism_check'),
    path('loading/<str:check_id>/', views.loading, name='loading'),
    path('process/<str:check_id>/', views.process_check, name='process_check'),
    path('results/<str:check_id>/', views.results, name='results'),
]