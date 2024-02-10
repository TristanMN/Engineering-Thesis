import numpy as np
import librosa
import os
import spectrummidi
import matplotlib.pyplot as plt

# audio_path = os.path.join(r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis")
# file_path = audio_path + "\\output.mp3"


global file


def main(file_path):
    # load audio
    name = os.path.splitext(os.path.basename(file_path))[0]
    y, sr = librosa.load(file_path)

    n_fft = np.power(2, 14)
    hop_length = int(n_fft / 64)
    # Fourier transformat
    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

    # converting to decibels
    D_db = librosa.amplitude_to_db(abs(D))

    times = librosa.times_like(D_db, hop_length=hop_length)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    # start finding tones
    global file
    file = spectrummidi.main(name, D_db, times, freqs, 1)

    # ploting spectrum

    # # D_db = np.maximum(D_db,0)
    # plt.figure(figsize=(24, 12))
    # # librosa.display.specshow(np.power(np.minimum(D_db,28),2)/np.power(int(np.minimum(D_db,28).max()),1), x_axis='time', y_axis='log', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
    # librosa.display.specshow(D_db, y_axis='log', x_axis='time', sr=sr, cmap='viridis', n_fft=n_fft, hop_length=hop_length)
    # plt.colorbar(format='%+2.0f dB')
    # plt.title("Spektrogram")
    # plt.xlabel("Czas (s)")
    # plt.ylabel("Częstotliwość (Hz)")
    # plt.savefig(str(name) + ".png")
    # plt.show()

    # phase = np.angle(D)

    # plt.figure(figsize=(24, 12))
    # librosa.display.specshow(phase, x_axis='time', sr=sr, cmap='viridis', n_fft = n_fft, hop_length = hop_length)
    # plt.colorbar(format='%+2.0f rad')
    # plt.title('Faza')
    # plt.xlabel('Czas (s)')
    # plt.ylabel('Częstotliwość (Hz)')
    # plt.savefig("wykresfazy.png")
    # plt.show()


# file_path = r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis\widma\hall\org\Rufus Wainwright - Hallelujah.mp3"
# main(file_path)


