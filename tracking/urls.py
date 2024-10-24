from django.urls import path
from . import views

urlpatterns = [
    # Home or tracking URL
    path('', views.track_url, name='track_url'),

    # Signup URL
    path('signup/', views.track_url, name='signup'),
]
