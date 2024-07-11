from django.shortcuts import render

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
    return render(request, 'Sign_in.html')

def register(request):
    return render(request, 'register.html')

def mimiking(voice, gender, convert_to):
    y, sr = librosa.load(voice)
    if gender==1:
        # man_pitch = man_voice(y, sr)
        if convert_to==0: # 0 for woman
            woman_dub = train_voice(y, sr, 3.64) # 3.64 for man to woman
        elif convert_to==2: # 2 for child
            child_dub = train_voice(y, sr, 5.89) # 5.89 for man to child
    else:
        # woman_pitch = woman_voice(y, sr)
        if convert_to==1: # 1 for man
            train_voice(y, sr, -0.014) # -0.014 for woman to man
        elif convert_to==2: # 2 for child
            train_voice(y, sr, 5.89) # 5.89 for woman to child
    
def train_voice(y1, sr1, n_step):
    new_voice = librosa.effects.pitch_shift(y1, n_steps= n_step, sr=sr1)

    new_voice = new_voice * 0.2
    nyquist = 0.5 * sr1
    cutoff_freq = 5000
    normal_cutoff = cutoff_freq / nyquist
    b, a = scipy.signal.butter(5, normal_cutoff, btype='low', analog=False)
    
    new_voice = scipy.signal.lfilter(b, a, new_voice)
    
    return new_voice