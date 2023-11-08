import pygame.midi
import numpy as np


def main():
    global song
    song = []
    pygame.midi.init()

    print("MIDI Input Devices:")
    input_device_id = None

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
            times = np.zeros((len(tons),len(tons)))
            time = 0
#            while True:
            while time < 40*1000:
                if midi_input.poll():
                    midi_events = midi_input.read(10)
                    note = midi_events[0][0][1]
                    ampli = midi_events[0][0][2]
                    time = midi_events[0][1]

                    if ampli > 0:
                        song.append(('note_on', midi_events[0][0][0], note, ampli, time))
#                        print(tons[note%12],int((note - note%12)/12), "Start")
                        times[int(note%12)][int((note - note%12)/12)] = time
                    if ampli == 0:
                        song.append(('note_off', midi_events[0][0][0], note, ampli, time))
                        print(tons[note%12],int((note - note%12)/12), "Stop", int(time - times[int(note%12)][int((note - note%12)/12)]),"ms", time)
        except KeyboardInterrupt:
            pass
    else:
        print("No valid MIDI input devices found.")
    pygame.midi.quit()
    return song

#main()