#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import mido
import fouriertry

freqs = fouriertry.freqs
spec = fouriertry.D_db
times = fouriertry.times
# tones = [4186.01, 4434.92, 4698.63, 4978.03, 5274.04, 5587.65, 5919.91, 6271.93, 6644.88, 7040, 7458.62, 7902.13]
# tones = tones[::-1]
# matrix = []
# for x in range(0, 9):
#     for ton in tones:
#         matrix.append(ton / np.power(2, x))
# matrix = matrix[::-1]
# print(matrix)
tones = [16.3516015625, 17.32390625, 18.3540234375, 19.4454296875, 20.60171875, 21.8267578125, 23.1246484375, 24.4997265625, 25.9565625, 27.5, 29.135234375, 30.8676953125, 32.703203125, 34.6478125, 36.708046875, 38.890859375, 41.2034375, 43.653515625, 46.249296875, 48.999453125, 51.913125, 55.0, 58.27046875, 61.735390625, 65.40640625, 69.295625, 73.41609375, 77.78171875, 82.406875, 87.30703125, 92.49859375, 97.99890625, 103.82625, 110.0, 116.5409375, 123.47078125, 130.8128125, 138.59125, 146.8321875, 155.5634375, 164.81375, 174.6140625, 184.9971875, 195.9978125, 207.6525, 220.0, 233.081875, 246.9415625, 261.625625, 277.1825, 293.664375, 311.126875, 329.6275, 349.228125, 369.994375, 391.995625, 415.305, 440.0, 466.16375, 493.883125, 523.25125, 554.365, 587.32875, 622.25375, 659.255, 698.45625, 739.98875, 783.99125, 830.61, 880.0, 932.3275, 987.76625, 1046.5025, 1108.73, 1174.6575, 1244.5075, 1318.51, 1396.9125, 1479.9775, 1567.9825, 1661.22, 1760.0, 1864.655, 1975.5325, 2093.005, 2217.46, 2349.315, 2489.015, 2637.02, 2793.825, 2959.955, 3135.965, 3322.44, 3520.0, 3729.31, 3951.065, 4186.01, 4434.92, 4698.63, 4978.03, 5274.04, 5587.65, 5919.91, 6271.93, 6644.88, 7040.0, 7458.62, 7902.13]
tons = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
print(spec)

index_freqs = []
ton_index = 0
for ton in tones:
    i = 0
    min_val = 32768
    for freq in freqs:
        if freq < ton:
            min_val = abs(ton - freq)
        else:
            if abs(ton - freq) < min_val:
                index_freqs.append((i,str(tons[ton_index%12]) + str(int((ton_index - ton_index%12)/12))))
            else:
                index_freqs.append((i - 1,str(tons[ton_index%12]) + str(int((ton_index - ton_index%12)/12))))
            break
        i+=1
    ton_index += 1
print(index_freqs)
print(spec.shape)

#pętla po częstotliwościach tonów:
#   tworzymy liste na dany ton oraz zmienną czas
#   pętla po czasie:
#       jeżeli amplituda jest wystarczająco wysoka:
#           jeżeli amplituda nie spadła:
#               czas++
#           jeżeli spadła:
#               zapisujemy w liście
#               czas = 0

all_tones = np.zeros(len(index_freqs)).astype(list)
itemp = 0
song = []
for i in index_freqs:
    list_of_keys = []
    jtemp = 0
    temp_time = 0

    for j in range(len(spec[0])):
        print(spec[i[0]][j],temp_time)
        if spec[i[0]][j] > 32 and temp_time == 0:
            song.append(('note_on', 0, itemp+12, 100, int(jtemp*times[1]*1000)))
            temp_time += 1
        elif spec[i[0]][j] > 32:
            temp_time += 1
        elif spec[i[0]][j] <= 32 and temp_time > 0:
            song.append(('note_on', 0, itemp+12, 0, int(jtemp*times[1]*1000)))
            list_of_keys.append((i[0], (jtemp - temp_time) * times[1], temp_time * times[1]))
            temp_time = 0
        jtemp += 1
    all_tones[itemp] = list_of_keys
    itemp += 1
song.sort(key=lambda a: a[4])

midi_file = mido.MidiFile()
track = mido.MidiTrack()
temptime = 0
for line in song:
    track.append(mido.Message(line[0], channel = 0, note = line[2], velocity = line[3], time = line[4] - temptime))
    temptime = line[4]
midi_file.tracks.append(track)
print(track)
print(len(song))
print(song)
midi_file.save('fourier.midi')