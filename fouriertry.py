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

audio_path = os.path.join(r"E:\Cała muzyka\Muzyka\DJ'ka\Akademik\Disco")
audio_file = audio_path + "\\Track No07.wav"
# audio_path = os.path.join(r"E:\Cała muzyka\Muzyka\DJ'ka")
# audio_file = audio_path + "\\100 LAT.mp3"
#audio_path = os.path.join(r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis")
#audio_file = audio_path + "\\output.mp3"
#audio_file = audio_path + "\\AnothLove.mp3"

# Wczytaj audio przy użyciu librosa
y, sr = librosa.load(audio_file)

n_fft = np.power(2,14)
hop_length = int(n_fft/4)
# Oblicz transformatę Fouriera
D = librosa.stft(y, n_fft = n_fft, hop_length = hop_length)

# Konwertuj amplitudę na decybele (dB)
D_db = librosa.amplitude_to_db(abs(D))
phase = np.angle(D)

times = librosa.times_like(D_db, hop_length = hop_length)
freqs = librosa.fft_frequencies(sr=sr, n_fft = n_fft)

# Wygeneruj wizualizację spektrogramu
plt.figure(figsize=(24, 12))
librosa.display.specshow(np.power(np.minimum(D_db,52),2)/np.power(int(np.minimum(D_db,52).max()),1), x_axis='time', y_axis='log', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
#librosa.display.specshow(D_db, x_axis='time', y_axis='log', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
plt.colorbar(format='%+2.0f dB')
plt.title("Spektrogram")
plt.xlabel("Czas (s)")
plt.ylabel("Częstotliwość (Hz)")
plt.savefig("wykresampli.png")
plt.show()

plt.figure(figsize=(24, 12))
librosa.display.specshow(phase, y_axis='log', x_axis='time', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
plt.colorbar(format='%+2.0f rad')
plt.title('Faza')
plt.xlabel('Czas (s)')
plt.ylabel('Częstotliwość (Hz)')
plt.savefig("wykresfazy.png")
plt.show()


print(D_db.shape, sr)
print("Wartości amplitudy:")
print(D_db)

print("\nWektor czasu:")
print(times)

print("\nWektor częstotliwości:")
print(freqs)
for x in freqs:
    print(x)
