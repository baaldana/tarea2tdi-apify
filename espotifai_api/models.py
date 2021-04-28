from django.db import models

# Create your models here.

class Artist(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=50)
    age = models.IntegerField()


class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)


class Track(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    duration = models.FloatField()
    times_played = models.IntegerField(default=0)
