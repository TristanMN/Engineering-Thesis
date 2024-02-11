import pygame
import pygame.midi
import numpy as np


def main():
    global song
    song = []
    pygame.init()
    pygame.midi.init()
    print("MIDI Input Devices:")
    input_device_id = None

    # finding the connected device
    for i in range(pygame.midi.get_count()):
        device_info = pygame.midi.get_device_info(i)
        print(device_info)
        if device_info[2]:
            print(f"{i}: {device_info[1].decode()}")
            if input_device_id is None:
                input_device_id = i

    if input_device_id is not None:
        midi_input = pygame.midi.Input(input_device_id)
        print(f"Receiving MIDI input from {pygame.midi.get_device_info(input_device_id)[1].decode()}")
        try:
            tons = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
            times_matrix = np.zeros((len(tons), 10))
            time = pygame.time.get_ticks()

            while time < 30 * 1000:  # time of recording
                time = int(pygame.time.get_ticks() * 24 / 25)  # convert shift time
                if midi_input.poll():
                    midi_events = midi_input.read(10)
                    note = midi_events[0][0][1]
                    ampli = midi_events[0][0][2]
                    timen = midi_events[0][1]
                    print(time, timen)
                    if ampli > 0:
                        song.append(('note_on', midi_events[0][0][0], note, ampli, time))
                        # print(tons[note%12],int((note - note%12)/12), "Start")
                        times_matrix[int(note % 12)][int((note - note % 12) / 12)] = time
                        print(tons[note % 12], int((note - note % 12) / 12), time, note,
                              "          ___________________")
                    if ampli == 0:
                        song.append(('note_off', midi_events[0][0][0], note, ampli, time))
                        print(tons[note % 12], int((note - note % 12) / 12),
                              int(time - times_matrix[int(note % 12)][int((note - note % 12) / 12)]), "ms", time, note,
                              "   |||||||||||||||||||")
        except KeyboardInterrupt:
            pass
    else:
        print("No valid MIDI input devices found.")
    pygame.midi.quit()
    return song

# main()
