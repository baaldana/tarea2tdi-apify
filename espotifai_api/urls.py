from django.urls import include, path
from . import views



urlpatterns = [ # 12 métodos
    path('artists/', views.artists_list, name='artists_list'),
    path('artists/<str:artist_id>', views.artist_detail, name='artist_detail'),
    path('artists/<str:artist_id>/tracks', views.artist_tracks, name='artist_tracks'),
    path('artists/<str:artist_id>/albums', views.artist_albums, name='artist_albums'), # 1 GET, POST
    path('albums/', views.albums_list, name='albums_list'),
    path('albums/<str:album_id>', views.album_detail, name='album_detail'), # 4 GET, DELETE
    path('artists/<str:artist_id>/albums/play', views.album_play, name='album_play'),
    path('artists/<str:album_id>/tracks', views.album_tracks, name='album_tracks'),
    path('tracks/', views.tracks_list, name='tracks_list'),
    path('tracks/<str:track_id>', views.track_detail, name='track_detail'),
    path('tracks/<str:track_id>/play', views.track_play, name='track_play'),
    path('artists/<str:artist_id>/tracks/play', views.track_play_all, name='track_play_all'),
]