#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from scipy.signal import butter, filtfilt
import librosa
import matplotlib.pyplot as plt

def butter_lowpass_filter(data, cutoff_frequency, sampling_rate, order=10):
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Wczytaj audio
audio_file = r"C:\Users\Tristan\Desktop\A Great Big World Christina Aguilera - Say Something.mp3"
y, sr = librosa.load(audio_file)

# Ogranicz częstotliwości do zakresu 0-5000 Hz
cutoff_frequency = 1000
filtered_audio = butter_lowpass_filter(y, cutoff_frequency, sr)

# Wygeneruj wizualizację sygnału przed i po filtracji
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(y)
plt.title('Sygnał audio przed filtracją')
plt.xlabel('Próbki')

plt.subplot(2, 1, 2)
plt.plot(filtered_audio)
plt.title('Sygnał audio po filtracji')
plt.xlabel('Próbki')

plt.tight_layout()
plt.show()

n_fft = np.power(2, 14)
hop_length = int(n_fft / 16)
# Oblicz transformatę Fouriera
D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

# Konwertuj amplitudę na decybele (dB)
D_db = librosa.amplitude_to_db(abs(D))

# Wygeneruj wizualizację spektrogramu
# D_db = np.maximum(D_db,0)
plt.figure(figsize=(24, 12))
# librosa.display.specshow(np.power(np.minimum(D_db,28),2)/np.power(int(np.minimum(D_db,28).max()),1), x_axis='time', y_axis='log', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
librosa.display.specshow(D_db, y_axis='log', x_axis='time', sr=sr / 2, cmap='viridis', n_fft=n_fft, hop_length=hop_length / 2)
plt.colorbar(format='%+2.0f dB')
plt.title("Spektrogram")
plt.xlabel("Czas (s)")
plt.ylabel("Częstotliwość (Hz)")
plt.show()

filtered_audio_D = librosa.stft(filtered_audio, n_fft=n_fft, hop_length=hop_length)

# Konwertuj amplitudę na decybele (dB)
filtered_audio_db = librosa.amplitude_to_db(abs(filtered_audio_D))

# Wygeneruj wizualizację spektrogramu
# D_db = np.maximum(D_db,0)
plt.figure(figsize=(24, 12))
# librosa.display.specshow(np.power(np.minimum(D_db,28),2)/np.power(int(np.minimum(D_db,28).max()),1), x_axis='time', y_axis='log', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
librosa.display.specshow(filtered_audio_db, y_axis='log', x_axis='time', sr=sr / 2, cmap='viridis', n_fft=n_fft, hop_length=hop_length / 2)
plt.colorbar(format='%+2.0f dB')
plt.title("Spektrogram")
plt.xlabel("Czas (s)")
plt.ylabel("Częstotliwość (Hz)")
plt.show()

y_reconstructed = librosa.istft(filtered_audio_D)

reconstructed_audio_D = librosa.stft(y_reconstructed, n_fft=n_fft, hop_length=int(hop_length / 2))

# Konwertuj amplitudę na decybele (dB)
reconstructed_audio_db = librosa.amplitude_to_db(abs(reconstructed_audio_D))

# Wygeneruj wizualizację spektrogramu
# D_db = np.maximum(D_db,0)
plt.figure(figsize=(24, 12))
# librosa.display.specshow(np.power(np.minimum(D_db,28),2)/np.power(int(np.minimum(D_db,28).max()),1), x_axis='time', y_axis='log', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
librosa.display.specshow(reconstructed_audio_db, y_axis='log', x_axis='time', sr=sr / 2, cmap='viridis', n_fft=n_fft, hop_length=hop_length / 2)
plt.colorbar(format='%+2.0f dB')
plt.title("Spektrogram")
plt.xlabel("Czas (s)")
plt.ylabel("Częstotliwość (Hz)")
plt.show()