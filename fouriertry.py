#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import librosa
import os
import spectrummidi
import matplotlib.pyplot as plt

#audio_path = os.path.join(r"E:\Cała muzyka\Muzyka\DJ'ka\nowe")
#file_path = audio_path + "\\Imagine Dragons - Demons.mp3"
#audio_path = os.path.join(r"E:\Cała muzyka\Muzyka\DJ'ka")
#audio_path = os.path.join(r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis")
#file_path = audio_path + "\\output.mp3"
#file_path = audio_path + "\\fourier.mp3"
global file

def main(file_path):
    # Wczytaj audio przy użyciu librosa
    name = os.path.splitext(os.path.basename(file_path))[0]
    y, sr = librosa.load(file_path)

    n_fft = np.power(2,14)
    hop_length = int(n_fft/16)
    # Oblicz transformatę Fouriera
    D = librosa.stft(y, n_fft = n_fft, hop_length = hop_length)

    # Konwertuj amplitudę na decybele (dB)
    D_db = librosa.amplitude_to_db(abs(D))
    times = librosa.times_like(D_db, hop_length=hop_length)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    global file
    file = spectrummidi.main(name, D_db, times, freqs)

    # Wygeneruj wizualizację spektrogramu
    # D_db = np.maximum(D_db,0)
    plt.figure(figsize=(24, 12))
    # librosa.display.specshow(np.power(np.minimum(D_db,28),2)/np.power(int(np.minimum(D_db,28).max()),1), x_axis='time', y_axis='log', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
    librosa.display.specshow(D_db, y_axis='log', x_axis='time', sr=sr / 2, cmap='viridis', n_fft=n_fft, hop_length=hop_length / 2)
    plt.colorbar(format='%+2.0f dB')
    plt.title("Spektrogram")
    plt.xlabel("Czas (s)")
    plt.ylabel("Częstotliwość (Hz)")
    plt.savefig("wykresampli.png")
    plt.show()


# file_path = r"C:\Users\Tristan\Desktop\Amber Run - I Found (Lyrics).mp3"
# main(file_path)
#phase = np.angle(D)




#
# plt.figure(figsize=(24, 12))
# librosa.display.specshow(phase, x_axis='time', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
# plt.colorbar(format='%+2.0f rad')
# plt.title('Faza')
# plt.xlabel('Czas (s)')
# plt.ylabel('Częstotliwość (Hz)')
# plt.savefig("wykresfazy.png")
# plt.show()
#
#
# print(D_db.shape, sr)
# print("Wartości amplitudy:")
# print(D_db)
#
# print("\nWektor czasu:")
# print(times)
#
# print("\nWektor częstotliwości:")
# print(freqs)
