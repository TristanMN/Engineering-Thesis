import numpy as np
import mido
import os


# tones = [4186.01, 4434.92, 4698.63, 4978.03, 5274.04, 5587.65, 5919.91, 6271.93, 6644.88, 7040, 7458.62, 7902.13]
# tones = tones[::-1]
# matrix = []
# for x in range(0, 9):
#     for ton in tones:
#         matrix.append(ton / np.power(2, x))
# matrix = matrix[::-1]
# print(matrix)

def main(name, spec, times, freqs, method):
    # list of frequencies of tones
    tones = [16.3516015625, 17.32390625, 18.3540234375, 19.4454296875, 20.60171875, 21.8267578125, 23.1246484375,
             24.4997265625, 25.9565625, 27.5, 29.135234375, 30.8676953125, 32.703203125, 34.6478125, 36.708046875,
             38.890859375, 41.2034375, 43.653515625, 46.249296875, 48.999453125, 51.913125, 55.0, 58.27046875,
             61.735390625, 65.40640625, 69.295625, 73.41609375, 77.78171875, 82.406875, 87.30703125, 92.49859375,
             97.99890625, 103.82625, 110.0, 116.5409375, 123.47078125, 130.8128125, 138.59125, 146.8321875, 155.5634375,
             164.81375, 174.6140625, 184.9971875, 195.9978125, 207.6525, 220.0, 233.081875, 246.9415625, 261.625625,
             277.1825, 293.664375, 311.126875, 329.6275, 349.228125, 369.994375, 391.995625, 415.305, 440.0, 466.16375,
             493.883125, 523.25125, 554.365, 587.32875, 622.25375, 659.255, 698.45625, 739.98875, 783.99125, 830.61,
             880.0, 932.3275, 987.76625, 1046.5025, 1108.73, 1174.6575, 1244.5075, 1318.51, 1396.9125, 1479.9775,
             1567.9825, 1661.22, 1760.0, 1864.655, 1975.5325, 2093.005, 2217.46, 2349.315, 2489.015, 2637.02, 2793.825,
             2959.955, 3135.965, 3322.44, 3520.0, 3729.31, 3951.065, 4186.01, 4434.92, 4698.63, 4978.03, 5274.04,
             5587.65, 5919.91, 6271.93, 6644.88, 7040.0, 7458.62, 7902.13]
    tons = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

    index_freqs = []
    ton_index = 0

    # findinging the closest frequencies to tones
    for ton in tones:
        i = 0
        min_val = np.inf
        for freq in freqs:
            if freq < ton:
                min_val = abs(ton - freq)
            else:
                if abs(ton - freq) < min_val:
                    index_freqs.append((i, str(tons[ton_index % 12]) + str(int((ton_index - ton_index % 12) / 12))))
                else:
                    index_freqs.append((i - 1, str(tons[ton_index % 12]) + str(int((ton_index - ton_index % 12) / 12))))
                break
            i += 1
        ton_index += 1

    print(spec.shape)

    itemp = 0
    song = []
    dBmax = np.amax(spec)
    shape = spec.shape

    dBthreshold = dBmax * 0.66  # parameter detecting tones
    param1, param2 = (0.4, 0.6)  # parameters detecting tones with 2nd, 3rd method
    if method == 2:  # calculating means of columns
        meanall = [np.mean(col) for col in spec.T]

    # main loop searching tones

    for i in index_freqs:  # by frequencies
        songtone = []
        jtemp = 0
        temp_time = 0
        dBprev = 0
        dBpasttemp = dBprev
        # listaczest = [str(tones[itemp]) + " " +str(tons[itemp%12]) + str((itemp-(itemp%12))/12)]

        for j in range(len(spec[0])):
            # listaczest.append((spec[i[0]][j], (float(int(times[jtemp]*100))/100)))

            if method == 2:
                tempmean = np.mean(meanall[max(j - 20, 0):min(j + 20, shape[1])])
                dBthreshold = (tempmean * param1 + dBmax * (1 - param1)) / param2

            if method == 3:
                tempmean = np.mean(spec[i[0] - 4:i[0] + 4, max(j - 20, 0):min(j + 20, shape[1])])
                dBthreshold = (tempmean * param1 + dBmax * (1 - param1)) / param2

            # if spec[i[0]][j] > dBthreshold/1.2:
            #     print(spec[i[0]][j], temp_time, i, times[jtemp])

            # detect local maximum
            if dBprev > spec[i[0]][j] > dBthreshold and dBpasttemp < dBprev > dBthreshold and temp_time == 0:
                jj = 0
                add = True
                # searching start of bound
                while spec[i[0]][j - jj] - spec[i[0]][j - jj - 1] > 0:
                    jj += 1
                for harmony in [12, 19, 24]:  # checking harmonic sounds
                    try:
                        for sound in song[itemp - harmony]:  # delete tone when it's harmonic
                            if sound[3] > 0 and sound[4] in [int(times[jtemp - 3 - jj] * 1000),
                                                             int(times[jtemp - 2 - jj] * 1000),
                                                             int(times[jtemp - 1 - jj] * 1000)]:
                                add = False
                                continue
                    except:
                        pass
                if add is True:  # detect tone and add when isn't harmonic
                    songtone.append(('note_on', 0, itemp + 12, 100, int(times[jtemp - 1 - jj] * 1000)))
                    temp_time += 2 + jj


            # detect local minimum after local maximum
            elif dBprev > spec[i[0]][j] > dBthreshold and dBpasttemp < dBprev > dBthreshold and temp_time > 0:
                add = True
                for harmony in [12, 19, 24]:  # checking harmonic sounds
                    try:
                        for sound in song[itemp - harmony]:  # not detect tone when it's harmonic
                            if sound[3] > 0 and sound[4] in [int(times[jtemp - 3] * 1000), int(times[jtemp - 2] * 1000),
                                                             int(times[jtemp - 1] * 1000)]:
                                add = False
                                continue
                    except:
                        pass
                if add is True:  # detect tone and add when isn't harmonic
                    songtone.append(('note_off', 0, itemp + 12, 0, int(times[jtemp - 2] * 1000)))
                    songtone.append(('note_on', 0, itemp + 12, 100, int(times[jtemp - 1] * 1000)))
                    temp_time = 2
                if add is False:  # end beginning tone when it's harmonic
                    songtone.append(('note_off', 0, itemp + 12, 0, int(times[jtemp - 2] * 1000)))
                    temp_time = 0


            # keep tone
            elif dBprev > spec[i[0]][j] > dBthreshold * 0.8 and temp_time > 0:
                temp_time += 1


            # end of tone duration
            elif spec[i[0]][j] <= dBthreshold * 0.8 and temp_time > 0:
                songtone.append(('note_off', 0, itemp + 12, 0, int(times[jtemp] * 1000)))
                temp_time = 0

            dBpasttemp = dBprev
            dBprev = spec[i[0]][j]
            jtemp += 1

        # if (itemp - 5) % 12 == 0:   #only F
        # if itemp // 12 == 1:   #1st octav
        #    lista.append(listaczest)
        # elif itemp in [108,109]:  #added to list of freqs to check
        #     lista.append(listaczest)

        itemp += 1
        song.append(songtone)

    # for i in range(len(spec.T[0])):
    #     print(spec[i][1259], freqs[i], i)

    # adding and sorting list of tones and converting to midi
    song = [elem for elems in song for elem in elems if len(elems) > 0]
    song.sort(key=lambda a: a[4])
    midi_file = mido.MidiFile()
    track = mido.MidiTrack()
    temptime = 0

    for line in song:
        track.append(mido.Message(line[0], channel=0, note=line[2], velocity=line[3], time=line[4] - temptime))
        temptime = line[4]
    midi_file.tracks.append(track)

    print(len(song))

    file = name + '.midi'  # + "_conv" + str(method)
    midi_file.save(file)

    current_directory = os.path.dirname(os.path.abspath(file))  # path of current folder
    file_path = os.path.join(current_directory, file)

    # TESTS
    # file = open('items.txt', 'w')
    # for item in lista:
    #     print(item)
    #     file.write(str(item) + "\n")
    # file.close()

    return file_path
