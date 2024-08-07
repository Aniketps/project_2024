from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.IntegerField()
    song_state = models.BooleanField()
    artist = models.CharField(max_length=50)
    album = models.CharField(max_length=50)
    track = models.CharField(max_length=10000)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class VirtualEnvironment(models.Model):
    owner = models.ForeignKey(User, related_name='owned_sessions', on_delete=models.CASCADE)
    # song = models.ForeignKey(Song, on_delete=models.CASCADE)
    listeners = models.ManyToManyField(User, related_name='listening_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session by {self.owner.username}"

class CurrentSong(models.Model):
    virtual_environment = models.OneToOneField(VirtualEnvironment, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    current_time = models.DateTimeField()

    def __str__(self):
        return f"Current song in {self.virtual_environment} is {self.song.title}"
