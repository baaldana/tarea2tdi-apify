from rest_framework import serializers
from .models import Artist, Album, Track

class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist 
        fields = [
            'id',
            'name',
            'age'
        ]

class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = [
            'id',
            'artist',
            'name',
            'genre',
        ]

class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = [
            'id',
            'album',
            'duration',
            'times_played',
        ]