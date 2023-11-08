#!/usr/bin/python
# -*- coding: utf-8 -*-
import pydub
import numpy as np
import scipy
import librosa
import os
import plotly.express as px
import librosa.display
import matplotlib.pyplot as plt

# audio_path = os.path.join(r"E:\Cała muzyka\Muzyka\DJ'ka\Akademik\Disco")
# audio_file = audio_path + "\\36.Gigi D' Agostino - L' Amour Toujours.mp3"
# audio_path = os.path.join(r"E:\Cała muzyka\Muzyka\DJ'ka")
# audio_file = audio_path + "\\100 LAT.mp3"
audio_path = os.path.join(r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis")
audio_file = audio_path + "\\output.mp3"

# Wczytaj audio przy użyciu librosa
y, sr = librosa.load(audio_file)

# Oblicz transformatę Fouriera
D = librosa.stft(y)

# Konwertuj amplitudę na decybele (dB)
D_db = librosa.amplitude_to_db(abs(D))

# Wygeneruj wizualizację spektrogramu
plt.figure(figsize=(24, 12))
librosa.display.specshow(D_db, x_axis='time', y_axis='log', sr=sr, cmap='viridis')
plt.colorbar(format='%+2.0f dB')
plt.title("Spektrogram")
plt.xlabel("Czas (s)")
plt.ylabel("Częstotliwość (Hz)")
plt.savefig("wykres.png")
plt.show()