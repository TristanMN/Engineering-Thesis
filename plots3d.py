import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ast
import os
import glob

file_path = r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis\Testy\third"
list_of_files = []
pattern = os.path.join(file_path, "*.txt")
list_of_files.extend(glob.glob(pattern))


def take_data_from_file(name):
    with open(name, 'r') as file:
        lines = file.readlines()

    data = [ast.literal_eval(line.strip()) for line in lines]
    size = np.shape(data)

    z, x, y = [], [], []
    for line_data in data:
        z_line, x_line, y_line = zip(*line_data)
        z.extend(z_line)
        x.extend(x_line)
        y.extend(y_line)
        norm = plt.Normalize(min(z), 2500)
        z = [val if val <= 2500 else 2500 for val in z]
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    x = np.reshape(x, (size[0], size[1]))
    y = np.reshape(y, (size[0], size[1]))
    z = np.reshape(z, (size[0], size[1]))

    return x, y, z, norm


fig, axs = plt.subplots(3, 3, figsize=(20, 20), subplot_kw={'projection': '3d'})

for i, name in enumerate(list_of_files):
    x, y, z, norm = take_data_from_file(name)
    wiersz = i // 3
    kolumna = i % 3

    axs[wiersz, kolumna].set_zlim([0, 2500])
    my_cmap = plt.get_cmap('magma')
    surf = axs[wiersz, kolumna].plot_surface(y, x, z, cmap=my_cmap, norm=norm, edgecolor='none')
    next = fig.colorbar(surf, ax=axs[wiersz, kolumna], pad=0.05, shrink=0.5, aspect=10, anchor=(1.7, 0.5))
    axs[wiersz, kolumna].set_box_aspect([1, 1, 0.5])
    axs[wiersz, kolumna].set_ylabel('Współczynnik proporcji\nśredniej oraz dB maks', labelpad=12)
    axs[wiersz, kolumna].set_xlabel('Dzielnik')
    axs[wiersz, kolumna].set_zlabel('Ilość znalezionych tonów')
    axs[wiersz, kolumna].set_title(f'{os.path.splitext(os.path.basename(name))[0]}')
    axs[wiersz, kolumna].grid(True)

plt.savefig("Zbiór wykresów łokciowych dla dB all")
plt.show()
