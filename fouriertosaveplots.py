import numpy as np
import librosa
import os
import matplotlib.pyplot as plt

def main(file_paths, num, name):
    # # fig, axs = plt.subplots(2, 2, figsize=(20, 10))
    # for i, file_path in enumerate(file_paths):
    #     row = i // 2
    #     col = i % 2
    y, sr = librosa.load(file_paths)

    n_fft = np.power(2, 14)
    hop_length = int(n_fft/16)
    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    D_db = librosa.amplitude_to_db(abs(D))
    D_db = np.maximum(D_db, 0)

    plt.subplot(2, 2, num)
    librosa.display.specshow(D_db, y_axis='log', x_axis='time', sr=sr, cmap='viridis', n_fft=n_fft,
                             hop_length=hop_length)
    plt.colorbar(format='%+2.0f dB')
    plt.title(f"Spektrogram {name}")
    plt.xlabel("Czas (s)")
    plt.ylabel("Częstotliwość (Hz)")

        # plt.subplot(2, 2, file_paths.index(file_path) + 1)
        # axs[row, col] = librosa.display.specshow(D_db, y_axis='log', x_axis='time', sr=sr, cmap='viridis', n_fft=n_fft, hop_length=hop_length)
        # # axs[row, col].set_xlabel("Czas (s)")
        # # axs[row, col].set_ylabel("Częstotliwość (Hz)")
        # # axs[row, col].set_title(name)
        # next = plt.colorbar(ax=axs[row, col], format='%+2.0f dB')


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
