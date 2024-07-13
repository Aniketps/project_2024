from django.shortcuts import render
from django.http import JsonResponse
import os # temp
from django.conf import settings # temp
from django.core.files.storage import FileSystemStorage # temp
from .forms import AudioUploadForm
import soundfile as sf


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

def mimiking(voice, gender, convert_to):
    y, sr = librosa.load(voice)
    if gender==1:
        # man_pitch = man_voice(y, sr)
        if convert_to==0: # 0 for woman
            dub_voice = train_voice(y, sr, 3.64) # 3.64 for man to woman
        elif convert_to==2: # 2 for child
            dub_voice = train_voice(y, sr, 5.89) # 5.89 for man to child
    else:
        # woman_pitch = woman_voice(y, sr) 
        if convert_to==1: # 1 for man
            dub_voice = train_voice(y, sr, -4) # -0.014 for woman to man
        elif convert_to==2: # 2 for child
            dub_voice = train_voice(y, sr, 5.89) # 5.89 for woman to child
        
    return dub_voice
            
    
    
def train_voice(y1, sr1, n_step):
    new_voice = librosa.effects.pitch_shift(y1, n_steps= n_step, sr=sr1*1.2)

    new_voice = new_voice * 3.5 
    
    return new_voice