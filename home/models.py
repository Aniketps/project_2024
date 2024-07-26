from django.db import models


class user_table(models.Model):
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    password1 = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)
    song_id = models.IntegerField(max_length=100000000)
    song_album = models.CharField(max_length=50)
    song_time = models.IntegerField(max_length=500)
    
        
    def __str__(self):
        return self.username
    