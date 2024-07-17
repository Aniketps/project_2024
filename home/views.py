from django.shortcuts import render
from django.http import JsonResponse
import os # temp
from django.conf import settings # temp
from django.core.files.storage import FileSystemStorage # temp
from .forms import AudioUploadForm
import soundfile as sf
from .mimiking import mimiking
from .tune import tune



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
# end mimiking import


# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

def frontend(request):
    return render(request, 'frontend.html')


def recommendation(request): 
    return render(request, 'recommendation.html')

def listen2gether(request):
    return render(request, "listen2gether.html")

def mimicking_page(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['audio_file']
            conversion_type = form.cleaned_data.get('conversion_type', None)

            y, sr = librosa.load(audio_file.temporary_file_path() if hasattr(audio_file, 'temporary_file_path') else audio_file)
            output_file = os.path.join(settings.BASE_DIR, 'home', 'static', 'uploads', 'mikicking', f'{audio_file.name.split(".")[0]}.wav')
            sf.write(output_file, y, sr)

            
            # ready = mimiking(output_file, 0, 1)
              
            if conversion_type == 'male_to_female':
                ready = mimiking(output_file, 1, 0)
            elif conversion_type == 'male_to_child':
                ready = mimiking(output_file, 1, 2)
            elif conversion_type == 'female_to_male':
                ready = mimiking(output_file, 0, 1)
            elif conversion_type == 'female_to_child':
                ready = mimiking(output_file, 0, 2)  
            else:
                 
                return JsonResponse({'message': 'Invalid conversion type'}, status=400)
 
            mimicked_output_file = os.path.join(settings.BASE_DIR, 'home', 'static', 'uploads', 'mikicking', f'{output_file.split(".")[0]}_mimicked.wav')
            sf.write(mimicked_output_file, ready, sr)
                        
            download_url = f'/static/uploads/mimicking/{os.path.basename(mimicked_output_file)}'
            
            return JsonResponse({'download_url': download_url})
        else:
            return JsonResponse({'message': 'Form is not valid', 'error': f'{form.errors}'}, status=400)
    else:
        form = AudioUploadForm()

    return render(request, 'mimicking.html', {'form': form})

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