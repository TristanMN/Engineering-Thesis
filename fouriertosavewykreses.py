#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import librosa
import os
import matplotlib.pyplot as plt

def main(file_paths, num, name):
    # # fig, axs = plt.subplots(2, 2, figsize=(20, 10))
    # for i, file_path in enumerate(file_paths):
    #     wiersz = i // 2
    #     kolumna = i % 2
        # Wczytaj audio przy użyciu librosa
    y, sr = librosa.load(file_paths)

    n_fft = np.power(2, 14)
    hop_length = int(n_fft/16)

    # Oblicz transformatę Fouriera
    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

    # Konwertuj amplitudę na decybele (dB)
    D_db = librosa.amplitude_to_db(abs(D))

    # Wygeneruj wizualizację spektrogramu
    D_db = np.maximum(D_db, 0)


    # Wyświetl widmo
    plt.subplot(2, 2, num)
    librosa.display.specshow(D_db, y_axis='log', x_axis='time', sr=sr, cmap='viridis', n_fft=n_fft,
                             hop_length=hop_length)
    plt.colorbar(format='%+2.0f dB')
    plt.title(f"Spektrogram {name}")
    plt.xlabel("Czas (s)")
    plt.ylabel("Częstotliwość (Hz)")

        # Wyświetl spektrogram
        # plt.subplot(2, 2, file_paths.index(file_path) + 1)
        # axs[wiersz, kolumna] = librosa.display.specshow(D_db, y_axis='log', x_axis='time', sr=sr, cmap='viridis', n_fft=n_fft, hop_length=hop_length)
        # # axs[wiersz, kolumna].set_xlabel("Czas (s)")
        # # axs[wiersz, kolumna].set_ylabel("Częstotliwość (Hz)")
        # # axs[wiersz, kolumna].set_title(name)
        # next = plt.colorbar(ax=axs[wiersz, kolumna], format='%+2.0f dB')


# Przykładowe użycie z listą ścieżek do 4 plików audio
file_paths_list = ['.mp3', '_conv1.mp3', '_conv2.mp3', '_conv3.mp3']
file_path = r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis\widma\fall\org\Michael Schulte - Falling Apart"

plt.figure(figsize=(24, 12))
name = os.path.splitext(os.path.basename(file_path))[0]
napisy = ["", " metoda 1", " metoda 2", " metoda 3"]
for i in range(4):
    print(i)
    file_paths_list[i] = file_path + file_paths_list[i]
    main(file_paths_list[i], i+1, name + napisy[i])
plt.tight_layout()
print(name)
plt.savefig(name)
plt.show()
