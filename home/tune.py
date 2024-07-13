import librosa
import IPython.display as ipd
import numpy as np
import pandas as pd
import soundfile as sf
import os

def tune(instrument, voice):
    if instrument == 1:  # 1 is piano
        data = piano_tune(voice)
    else:
        data = guitar_tune(voice)
    return data

def piano_tune(voice):
    y, sr = librosa.load(voice, sr=None)
    
    first_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=-15)
    second_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=-10)
    third_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=-5)
    fourth_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=5)
    fifth_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=10)
    
    final_piano = [first_voice, second_voice, third_voice, fourth_voice, fifth_voice]
    return final_piano

def guitar_tune(voice):
    y, sr = librosa.load(voice)
    
    second_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=-10)
    third_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=-5)
    fourth_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=5)
    fifth_voice = librosa.effects.pitch_shift(y, sr=sr, n_steps=10)
    
    final_guitar = [second_voice, third_voice, fourth_voice, fifth_voice]
    return final_guitar
