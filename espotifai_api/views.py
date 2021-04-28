from django.shortcuts import render
from .models import Artist, Album, Track
from rest_framework import generics, status
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer

# Create your views here.

# Artist Endpoints

def artist_list(request):
    if request.method == 'GET':
        artists = Artist.objects.all()
        artists_serializer = ArtistSerializer(artists, many=True)
        return JsonResponse(artists_serializer.data, safe=False)

    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


def artist_detail(request, pk):
    try: 
        artist = Artist.objects.get(pk=pk) 
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

