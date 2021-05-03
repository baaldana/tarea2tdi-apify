from django.shortcuts import render
from base64 import b64encode, b64decode
from .models import Artist, Album, Track
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.response import Response
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from espotifai.settings import API_HOST

# Create your views here.
api_host_url = API_HOST
#api_host_url = 'http://127.0.0.1:8000/'

@api_view(['GET', 'POST']) # obtener todos los artistas y crear
def artists_list(request):
    if request.method == 'GET':
        artists = Artist.objects.all()
        artists_serializer = ArtistSerializer(artists, many=True)
        response = []
        for artist in artists_serializer.data:
            albums_url = f'{api_host_url}artists/{artist["id"]}/albums'
            tracks_url = f'{api_host_url}artists/{artist["id"]}/tracks'
            self_url = f'{api_host_url}artists/{artist["id"]}'
            data = {
                'id': artist['id'],
                'name': artist['name'],
                'age': artist['age'],
                'albums': albums_url,
                'tracks': tracks_url,
                'self': self_url
            }
            response.insert(0, data)
        return JsonResponse(response, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if not data or len(data) < 2:
            return Response({'message': 'Request body is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        artist_id = b64encode(data['name'].encode()).decode('utf-8')[:22]
        try:
            Artist.objects.get(pk=artist_id)
            print("Ya existe el ID")
            return Response({'message': 'An existing artist already has that ID'}, status=status.HTTP_409_CONFLICT)
        except Artist.DoesNotExist:
            pass
        data = {'id': artist_id, **data} # Para ordenar el dict y se despliegue en el orden correspondiente
        artist_serializer = ArtistSerializer(data=data)
        if artist_serializer.is_valid():
            artist_serializer.save()
            albums_url = f'{api_host_url}artists/{artist_id}/albums'
            tracks_url = f'{api_host_url}artists/{artist_id}/tracks'
            self_url = f'{api_host_url}artists/{artist_id}'
            data = {
                'id': data['id'],
                'name': data['name'],
                'age': data['age'],
                'albums': albums_url,
                'tracks': tracks_url,
                'self': self_url
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(artist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['GET', 'DELETE']) # Obtener y borrar un artista
def artist_detail(request, artist_id):
    try: 
        artist = Artist.objects.get(pk=artist_id)
    except Artist.DoesNotExist: 
        return JsonResponse(
            {'message': 'The artist does not exist'},
            status=status.HTTP_404_NOT_FOUND
        ) 

    if request.method == 'GET':
        artist_serializer = ArtistSerializer(artist, many=False)
        albums = f'{api_host_url}artists/{artist_id}/albums'
        tracks = f'{api_host_url}artists/{artist_id}/tracks'
        self_url = f'{api_host_url}artists/{artist_id}'
        response = JsonResponse(
            {
            **artist_serializer.data,
            'albums': albums,
            'tracks': tracks,
            'self': self_url
            },
            safe=False)
        return response

    elif request.method == 'DELETE':
        artist.delete()
        return Response({'message': 'The artist was deleted succesfully'} , status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['GET', 'POST']) # Obtener los albums de un artista y crear albums de ese artista
def artist_albums(request, artist_id):

    if request.method == 'GET':
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return JsonResponse(
                {'message': 'The artist does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        albums = Album.objects.filter(artist=artist_id)
        albums_serializer = AlbumSerializer(albums, many=True)
        response = []
        for album in albums_serializer.data:
            # FIX DICT ORDER FOR OUTPUT
            artist_url = f'{api_host_url}artists/{album["artist"]}'
            tracks_url = f'{api_host_url}albums/{album["id"]}/tracks'
            self_url = f'{api_host_url}albums/{album["id"]}'
            data = {
                'id': album['id'],
                'artist_id': artist_id,
                'name': album['name'],
                'genre': album['genre'],
                'artist': artist_url,
                'tracks': tracks_url,
                'self': self_url
            }
            response.insert(0, data)

        return JsonResponse(response, safe=False)

    elif request.method == 'POST':
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return JsonResponse(
                {'message': 'The artist does not exist'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        data = JSONParser().parse(request)
        if not data or len(data) < 2:
            return Response({'message': 'Request body is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        album_id = b64encode((f'{data["name"]}:{artist_id}').encode()).decode('utf-8')[:22]

        try:
            Album.objects.get(pk=album_id)
            print("Ya existe el ID")
            return Response({'message': 'An existing album already has that ID'}, status=status.HTTP_409_CONFLICT)
        except Album.DoesNotExist:
            pass
        data = {'id': album_id, 'artist': artist_id, **data} # Para ordenar el dict y se despliegue en el orden correspondiente
        album_serializer = AlbumSerializer(data=data)
        if album_serializer.is_valid():
            album_serializer.save()
            artist_url = f'{api_host_url}artists/{artist_id}/albums'
            tracks_url = f'{api_host_url}albums/{data["id"]}/tracks'
            self_url = f'{api_host_url}albums/{data["id"]}'
            data = {
                'id': data['id'],
                'artist_id': artist_id,
                'name': data['name'],
                'genre': data['genre'],
                'artist': artist_url,
                'tracks': tracks_url,
                'self': self_url
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['GET'])
def artist_tracks(request, artist_id): # Obtener todos los tracks de un artista
    try:
        artist = Artist.objects.get(pk=artist_id)
    except Artist.DoesNotExist:
        return JsonResponse(
            {'message': 'The artist does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        albums = Album.objects.filter(artist=artist_id)
        all_tracks = []
        for album in albums:
            tracks = Track.objects.filter(album=album.id)
            if tracks:
                tracks_serializer = TrackSerializer(tracks, many=True)
                for track in tracks_serializer.data:
                    track['artist'] = f'{api_host_url}artists/{artist_id}'
                    track['album'] = f'{api_host_url}albums/{album.id}'
                    track['self'] = f'{api_host_url}tracks/{track["id"]}'
                all_tracks = [*tracks_serializer.data,  *all_tracks]
        
        return JsonResponse(all_tracks, safe=False)

    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

# Album Endpoints

@api_view(['GET']) # Obtener todos los album 
def albums_list(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        albums_serializer = AlbumSerializer(albums, many=True)
        response = []
        for album in albums_serializer.data:
            artist_url = f'{api_host_url}artists/{album["artist"]}'
            tracks_url = f'{api_host_url}albums/{album["id"]}/tracks'
            self_url = f'{api_host_url}albums/{album["id"]}'
            data = {
                'id': album['id'],
                'artist_id': album['artist'],
                'name': album['name'],
                'genre': album['genre'],
                'artist': artist_url,
                'tracks': tracks_url,
                'self': self_url
            }
            response.insert(0, data)
        return JsonResponse(response, safe=False)

        
        albums_serializer = AlbumSerializer(albums, many=True)
        for album in albums_serializer.data:
            album['artist'] = f'{api_host_url}artists/{album["artist_id"]}'
            album['tracks'] = f'{api_host_url}albums/{album["id"]}/tracks'
            album['self'] = f'{api_host_url}albums/{album["id"]}'

        return JsonResponse(albums_serializer.data, safe=False)
    
    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['GET','DELETE']) # Obtener y borrar un album
def album_detail(request, album_id):
    try: 
        album = Album.objects.get(pk=album_id)
        artist = Artist.objects.get(pk=album.artist.id)
    except Album.DoesNotExist: 
        return JsonResponse(
            {'message': 'The album does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Artist.DoesNotExist:
        return JsonResponse(
            {'message': 'The artist does not exist'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    if request.method == 'GET':
        artist_url = f'{api_host_url}artists/{artist.id}'
        tracks_url = f'{api_host_url}albums/{album_id}/tracks'
        self_url = f'{api_host_url}albums/{album_id}'
        response = JsonResponse(
            {
            'id': album.id,
            'artist_id': artist.id,
            'name': album.name,
            'genre': album.genre,
            'artist': artist_url,
            'tracks': tracks_url,
            'self': self_url
            },
            safe=False)
        return response

    elif request.method == 'DELETE':
        album.delete()
        return Response({'message': 'The album was deleted succesfully'} , status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['GET', 'POST']) # Obtener todas las tracks de un album o crear una track de un album
def album_tracks(request, album_id):
    #Revisar si existe el album id
    try:
        album = Album.objects.get(pk=album_id)
        artist = Artist.objects.get(pk=album.artist.id)
    except Album.DoesNotExist:
        return JsonResponse(
            {'message': 'The album does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Artist.DoesNotExist:
        return JsonResponse(
            {'message': 'The artist does not exist'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    if request.method == 'GET':
        tracks = Track.objects.filter(album=album_id)
        tracks_serializer = TrackSerializer(tracks, many=True)
        response = []
        for track in tracks_serializer.data:
            artist_url = f'{api_host_url}artists/{artist.id}'
            album_url = f'{api_host_url}albums/{album_id}'
            self_url = f'{api_host_url}tracks/{track["id"]}'
            data = {
                'id': track['id'],
                'album_id': album_id,
                'name': track['name'],
                'duration': track['duration'],
                'times_played': track['times_played'],
                'artist': artist_url,
                'album': album_url,
                'self': self_url
            }
            response.insert(0, data)
        return JsonResponse(response, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if not data or len(data) < 2:
            return Response({'message': 'Request body is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        track_id = b64encode((f'{data["name"]}:{album_id}').encode()).decode('utf-8')[:22]
        try:
            Track.objects.get(pk=track_id)
            print("Ya existe el ID")
            return Response({'message': 'An existing track already has that ID'}, status=status.HTTP_409_CONFLICT)
        except Track.DoesNotExist:
            pass

        data = {'id': track_id, 'album': album_id, **data, 'times_played': 0} # Para ordenar el dict y se despliegue en el orden correspondiente
        track_serializer = TrackSerializer(data=data)
        if track_serializer.is_valid():
            track_serializer.save()
            artist_url = f'{api_host_url}artists/{artist.id}'
            album_url = f'{api_host_url}albums/{album_id}'
            self_url = f'{api_host_url}tracks/{track_id}'
            data = {
                'id': data['id'],
                'album_id': album_id,
                'name': data['name'],
                'duration': data['duration'],
                'times_played': data['times_played'],
                'artist': artist_url,
                'album': album_url,
                'self': self_url
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(track_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
# Track Endpoints

@api_view(['GET']) # Obtener todas las tracks
def tracks_list(request):
    if request.method == 'GET':
        tracks = Track.objects.all()
        tracks_serializer = TrackSerializer(tracks, many=True)
        response = []
        for track in tracks_serializer.data:
            album =  Album.objects.get(pk=track['album'])
            artist = Artist.objects.get(pk=album.artist.id)
            artist_url = f'{api_host_url}artists/{artist.id}'
            album_url = f'{api_host_url}albums/{album.id}'
            self_url = f'{api_host_url}tracks/{track["id"]}'
            data = {
                'id': track['id'],
                'album_id': album.id,
                'name': track['name'],
                'duration': track['duration'],
                'times_played': track['times_played'],
                'artist': artist_url,
                'album': album_url,
                'self': self_url
            }
            response.insert(0, data)
        return JsonResponse(response, safe=False)

    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['GET', 'DELETE']) # Obtener y crear tracks
def track_detail(request, track_id):
    try:
        track = Track.objects.get(pk=track_id)
    except Track.DoesNotExist:
        return JsonResponse(
            {'message': 'The track does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        album = Album.objects.get(pk=track.album.id)
        artist = Artist.objects.get(pk=album.artist.id)
        artist_url = f'{api_host_url}artists/{artist.id}'
        album_url = f'{api_host_url}albums/{album.id}'
        self_url = f'{api_host_url}tracks/{track_id}'
        data = {
            'id': track.id,
            'album_id': album.id,
            'name': track.name,
            'duration': track.duration,
            'times_played': track.times_played,
            'artist': artist_url,
            'album': album_url,
            'self': self_url
        }
        return JsonResponse(data, safe=False)
    elif request.method == 'DELETE':
        track.delete()
        return Response({'message': 'The track was deleted succesfully'} , status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

# Play Endpoints

@api_view(['PUT']) # Reproducir una track
def track_play(request, track_id):
    try: 
        track = Track.objects.get(pk=track_id)
    except Track.DoesNotExist: 
        return JsonResponse(
            {'message': 'The track does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'PUT':
        track.times_played += 1
        track.save()
        return Response({'message': 'The track was played succesfully'} , status=status.HTTP_200_OK)
    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['PUT']) # Reproducir todas las tracks de un album
def album_play(request, album_id):
    try: 
        album = Album.objects.get(pk=album_id)
    except Album.DoesNotExist: 
        return JsonResponse(
            {'message': 'The album does not exist'},
            status=status.HTTP_404_NOT_FOUND
        ) 
    if request.method == 'PUT':
        tracks = Track.objects.filter(album=album_id)
        for track in tracks:
            track.times_played += 1
            track.save()
        return Response({'message': 'The tracks were played succesfully'} , status=status.HTTP_200_OK)
    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['PUT']) # Reproducir todas las tracks de un artista
def artist_play(request, artist_id):
    try: 
        artist = Artist.objects.get(pk=artist_id)
    except Artist.DoesNotExist: 
        return JsonResponse(
            {'message': 'The artist does not exist'},
            status=status.HTTP_404_NOT_FOUND
        ) 
    if request.method == 'PUT':
        albums = Album.objects.filter(artist=artist_id)
        for album in albums:
            tracks = Track.objects.filter(album=album.id)
            for track in tracks:
                track.times_played += 1
                track.save()
        return Response({'message': 'The tracks were played succesfully'} , status=status.HTTP_200_OK)
    else:
        return Response(
            {'message': f'{request.method} method not allowed for this request'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )