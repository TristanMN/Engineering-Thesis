#!/usr/bin/python
# -*- coding: utf-8 -*-

import scipy
import matplotlib as plt
import numpy as np
import librosa
import os
import glob
import plotly.express as px


audio_path = os.path.join(r"E:\Cała muzyka\Muzyka\DJ'ka\Akademik\Disco")

MP3_FILES = glob.glob(pathname=f'{audio_path}/*.mp3', recursive=True)
#for song in MP3_FILES:
def transform(song):
    audio, sample_rate = librosa.load(song)
    tempo, _ = librosa.beat.beat_track(y=audio, sr=sample_rate)
    print("Tempo ", song, f": {tempo} BPM")

    # Podziel sygnał na krótkie ramki
    frame_size = int(sample_rate * 0.025)  # Długość ramki (np. 25 ms)
    hop_size = int(sample_rate * 0.01)  # Skok między ramkami (np. 10 ms)
    frames = librosa.util.frame(audio, frame_length=frame_size, hop_length=hop_size)

    # Przeprowadź DFT na każdej ramce
    spectra = np.fft.fft(frames, axis=0)
    amplitudes = np.abs(spectra)

    # Wizualizacja widma amplitudowego
    fig = px.imshow(amplitudes, x=np.arange(amplitudes.shape[1]), y=np.arange(amplitudes.shape[0]), zmin=0,
                    aspect='auto')
    fig.update_layout(
        title="Widmo amplitudowe",
        xaxis_title="Czas (ramki)",
        yaxis_title="Częstotliwość (Hz)"
    )
    fig.show()

audio = audio_path + "\\MANDEE - COCO JAMBO 2016 (org. Mr. President).mp3"
transform(audio)