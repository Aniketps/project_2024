from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import os # temp
from django.conf import settings # temp
from django.core.files.storage import FileSystemStorage # temp
from .forms import AudioUploadForm, user_login, user_login1
from .models import user_table
import soundfile as sf
from .mimiking import mimiking
from .tune import tune
import requests
from django.views.decorators.csrf import csrf_exempt


# mimiking imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import librosa
import scipy

from glob import glob
import IPython.display as ipd
from IPython.display import Audio
import base64
# end mimiking import

def get_access_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    token_info = response.json()
    return token_info["access_token"]

# Replace with your actual credentials
CLIENT_ID = "be56693209714f688464c121d530d221"
CLIENT_SECRET = "fab2e9893dc54b96abcb390f39d950bc"

access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    form = user_login1()
    if request.method == 'POST':
        form = user_login1(request.POST)
        if form.is_valid:

            # cleaned_data = super().clean()
            
            # first_name = request.POST.get('first_name')
            # last_name = request.POST.get('last_name')
            # email = request.POST.get('email')
            # username = cleaned_data.get('username')
            # password1 = cleaned_data.get('password1')
            # password2 = cleaned_data.get('password2')
            
            # user1 = user_table(first_name=first_name, last_name=last_name, email=email, username=username, password=password2, song_id=0, song_album='None', song_time=0)
            
            form.save()
            return redirect('login')
    return render(request, 'register.html', {'form':form})

def login_page(request):
    return render(request, 'login_page.html')

def fetch_songs(query, limit=50):
    url = "https://api.spotify.com/v1/search"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": limit
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        songs = []
        tracks = data.get('tracks', {}).get('items', [])
        for track in tracks:
            name = track.get('name', 'Unknown')
            artist = track.get('artists', [{}])[0].get('name', 'Unknown')
            album = track.get('album', {}).get('name', 'Unknown')
            duration_ms = track.get('duration_ms', 0)
            added_at = track.get('added_at', 'Unknown')

            duration_min = duration_ms // 60000
            duration_sec = (duration_ms % 60000) // 1000
            duration = f"{duration_min}m {duration_sec}s"
            url = track.get('preview_url', 'No preview available')
            album_images = track.get('album', {}).get('images', [])
            image_url = album_images[1].get('url') if album_images else 'No image available'
            
            songs.append({
                "name": name,
                "artist": artist,
                "album": album,
                "duration": duration,
                "added_at": added_at,
                "url": url,
                "img_url": image_url
            })
            
        return songs

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def frontend(request):

    # if 'term' in request.GET:
    #     # search_query = request.POST.get('search')
    #     search_results = fetch_songs('mahi', limit=30)
        
    #     names = []
        
    #     for name in search_results:
    #         names.append(name['name'])
            
    #     print(names)
    #     print(type(names))
        
    #     return JsonResponse(name, safe = false)
        
    # if request.method == 'POST':
    #     search_query = request.POST.get('search')
    #     search_results = fetch_songs(search_query, limit=30)
          
    #     return render(request, 'frontend.html', {'seatch_result': search_results})
    
    
    trending_songs = fetch_songs("marathi", limit=50) 
    nineties_songs = fetch_songs("1990s hindi", limit=50)  
    todays_special_songs = fetch_songs("arijit singh", limit=50)  

    
    return render(request, 'frontend.html', {'trending_song_list': trending_songs,
                                             "s1990_song_list": nineties_songs,
                                             'special_song_list': todays_special_songs})
 

def recommendation(request): 
    return render(request, 'recommendation.html')

def piano(request):  
    return render(request, 'piano.html') 

def guitar(request): 
    return render(request, 'guitar.html')

def violien(request): 
    return render(request, 'violien.html') 

def listen2gether(request):
    
    contents = fetch_songs('Arjit Singh', limit=50) 
            
    return render(request, "listen2gether.html", {'contents': contents})  
 
    
@csrf_exempt
def mimicking_page(request):
    if request.method == 'POST':
        convert_to = request.POST.getlist('convert_to');
        
        input_voice = 0
        output_voice = 0
        
        if 'male_to_female' in convert_to:
            input_voice = 1
            output_voice = 0
        elif 'male_to_child' in convert_to:
            input_voice = 1
            output_voice = 2
        elif 'female_to_male' in convert_to:
            input_voice = 0
            output_voice = 1
        else:
            input_voice = 0
            output_voice = 2
            
        audio_file = request.FILES.get('audio_file') 
        if not audio_file:
            return HttpResponse("No audio file uploaded", status=400)

        try:
            y, sr = librosa.load(audio_file, sr=None) 
            output_file = mimiking(y,sr, input_voice, output_voice)
            save_path = os.path.join(settings.BASE_DIR,'home', 'static', 'uploads', 'mimicking', f'{audio_file.name.split(".")[0]}.wav')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            sf.write(save_path, output_file, sr)
            download_file = f'/static/uploads/mimicking/{audio_file.name.split(".")[0]}.wav'
            return JsonResponse({'download_url': download_file, 'title': audio_file.name.split(".")[0]})  
        except Exception as e:
            return HttpResponse(f"Error processing audio file: {e}", status=500) 
    else:
        return render(request, 'mimicking.html')

def tune_page(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['audio_file']
            
            # Process the audio file (example with librosa)
            try:
                y, sr = librosa.load(audio_file.temporary_file_path() if hasattr(audio_file, 'temporary_file_path') else audio_file)
                output_file_base = os.path.join(settings.BASE_DIR, 'home', 'static', 'uploads', 'tunes', f'{audio_file.name.split(".")[0]}')

                if not os.path.exists(output_file_base):
                    os.makedirs(output_file_base)

                ready = tune(1, audio_file)  # Adjust to pass the correct file path or file object

                download_urls = []
                for idx, processed_audio in enumerate(ready):
                    processed_output_file = f"{output_file_base}_converted_{idx+1}.wav"
                    sf.write(processed_output_file, processed_audio, sr)
                    download_url = f'/static/uploads/tunes/{os.path.basename(processed_output_file)}'
                    download_urls.append(download_url)

                return JsonResponse({'message': 'File uploaded successfully', 'download_urls': download_urls})
            
            except Exception as e:
                return JsonResponse({'message': 'Error processing file', 'error': str(e)}, status=500)
        
        else:
            return JsonResponse({'message': 'Form is not valid', 'error': form.errors}, status=400)
    
    else:
        form = AudioUploadForm()
    
    return render(request, 'tunes.html', {'form': form})