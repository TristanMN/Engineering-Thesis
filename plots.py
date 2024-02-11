import matplotlib.pyplot as plt
import os
import glob

file_path = r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis\Testy\first"
list_of_files = []

pattern = os.path.join(file_path, "*.txt")
list_of_files.extend(glob.glob(pattern))


def take_data_from_file(name):
    with open(name, 'r') as plik:
        lines = plik.readlines()
    dane = [eval(line.strip()) for line in lines]
    y, x = zip(*dane)
    return x, y


fig, axs = plt.subplots(3, 3, figsize=(20, 20))

for i, name in enumerate(list_of_files):
    x, y = take_data_from_file(name)
    wiersz = i // 3
    kolumna = i % 3
    axs[wiersz, kolumna].plot(x, y, marker='o', linestyle='-', label=f'Plik {i + 1}')
    axs[wiersz, kolumna].set_xlabel('Współczynnik przy maksymalnej wartości dB')
    axs[wiersz, kolumna].set_ylabel('Ilość znalezionych tonów')
    axs[wiersz, kolumna].set_title(f'{os.path.splitext(os.path.basename(name))[0]}')
    axs[wiersz, kolumna].grid(True)

plt.savefig("Zbiór wykresów łokciowych dla dB max")
fig.show()
