from django.shortcuts import render
from base64 import b64encode, b64decode
from .models import Artist, Album, Track
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.response import Response
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer

# Create your views here.

api_host_url = 'http://127.0.0.1:8000/'

@api_view(['GET', 'POST']) # obtener todos los artistas y crear
def artists_list(request):
    if request.method == 'GET':
        artists = Artist.objects.all()
        artists_serializer = ArtistSerializer(artists, many=True)
        return JsonResponse(artists_serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        artist_id = b64encode(data['name'].encode()).decode('utf-8')[:22]
        data = {'id': artist_id, **data} # Para ordenar el dict y se despliegue en el orden correspondiente
        artist_serializer = ArtistSerializer(data=data)
        if artist_serializer.is_valid():
            artist_serializer.save()
            albums_url = f'{api_host_url}artists/{artist_id}/albums'
            tracks_url = f'{api_host_url}artists/{artist_id}/tracks'
            self_url = f'{api_host_url}artists/{artist_id}'
            data = {**data, 'albums': albums_url, 'tracks': tracks_url, 'self': self_url}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(artist_serializer.errors, status=status.HTTP_408_BAD_REQUEST)

    else:
        pass

@api_view(['GET', 'DELETE']) # Obtener y borrar artista
def artist_detail(request, artist_id):
    try: 
        artist = Artist.objects.get(pk=artist_id) 
    except Tutorial.DoesNotExist: 
        return JsonResponse(
            {'message': 'The artist does not exist'},
            status=status.HTTP_404_NOT_FOUND
        ) 

    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

@api_view(['GET', 'POST']) # Obtener y crear albums
def artist_albums(request, artist_id):
    try:
        artist = Artist.objects.get(pk=artist_id)
    except Artist.DoesNotExist:
        return JsonResponse(
            {'message': 'The artist does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        print('inside get')
        albums = Album.objects.filter(artist=artist_id)
        print(albums)
        albums_serializer = AlbumSerializer(albums, many=True)
        return JsonResponse(albums_serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        album_id = b64encode((f'{data["name"]}:{artist_id}').encode()).decode('utf-8')[:22]
        data = {'id': album_id, 'artist_id': artist_id, **data} # Para ordenar el dict y se despliegue en el orden correspondiente
        album_serializer = AlbumSerializer(data=data)
        if album_serializer.is_valid():
            album_serializer.save()
            artist_url = f'{api_host_url}artists/{artist_id}/albums'
            tracks_url = f'{api_host_url}artists/{artist_id}/tracks'
            self_url = f'{api_host_url}artists/{artist_id}'
            data = {**data, 'artist_url': artist_url, 'tracks': tracks_url, 'self': self_url}
            return Response(album_serializer.errors, status=status.HTTP_201_CREATED)
        return Response(album_serializer.errors, status=status.HTTP_408_BAD_REQUEST)

def artist_tracks(request, artist_id): # Obtener todos los tracks de un artista
    pass



# Album Endpoints

@api_view(['GET']) # obtener todos los album 
def albums_list(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        albums_serializer = AlbumSerializer(albums, many=True)
        return JsonResponse(albums_serializer.data, safe=False)


@api_view(['GET','DELETE']) # Obtener y borrar un album
def album_detail(request, album_id):
    pass

@api_view(['PUT'])
def album_play(request, artist_id):
    pass

@api_view(['GET','POST'])
def album_tracks(request, album_id):
    pass

# Track Endpoints

@api_view(['GET', 'POST'])
def tracks_list(request):
    if request.method == 'GET':
        tracks = Track.objects.all()
        tracks_serializer = TrackSerializer(tracks, many=True)
        return JsonResponse(tracks_serializer.data, safe=False)

    elif request.method == 'POST':
        track_serializer = TrackSerializer(data=JSONParser().parse(request))
        if track_serializer.is_valid():
            track_serializer.save()
            return Response(track_serializer.data, status=status.HTTP_201_CREATED)
        return Response(track_serializer.errors, status=status.HTTP_408_BAD_REQUEST)


def track_detail(request, track_id):
    pass

def track_play(request, track_id):
    pass

def track_play_all(request, track_id):
    pass