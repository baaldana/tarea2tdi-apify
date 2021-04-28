from django.urls import include, path
from . import views



urlpatterns = [
    path('artists/', views.artist_list, name='artist_list'),
]