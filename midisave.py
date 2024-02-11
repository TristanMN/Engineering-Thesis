import mido
from midi import main

midi_file = mido.MidiFile()
track = mido.MidiTrack()
song = main()
temptime = 0
for line in song:
    track.append(mido.Message(line[0], channel=0, note=line[2], velocity=line[3], time=line[4] - temptime))
    temptime = line[4]
midi_file.tracks.append(track)
midi_file.save('prez.midi')
