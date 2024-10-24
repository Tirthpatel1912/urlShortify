from django.urls import path
from . import views

urlpatterns = [
    path('', views.shorten_url, name='shorten_url'),  # Shortening URL functionality
    path('search/', views.search_url, name='redirect_url'),  # Searching and redirecting functionality
]
