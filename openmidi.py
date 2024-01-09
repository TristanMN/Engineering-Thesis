import mido

def main(file):
    # Open a MIDI file
    #midi_file = mido.MidiFile('fourier.midi')
    #midi_file = mido.MidiFile('output.midi')
    #midi_file = mido.MidiFile('pianinko.midi')
    #midi_file = mido.MidiFile('Kodaline - All I Want.midi')
    #midi_file = mido.MidiFile('Tom Odell - Another Love.midi')
    midi_file = mido.MidiFile(file)
    # Create an empty list to store MIDI events as a matrix
    midi_matrix = []
    # Iterate through the tracks and messages and add them to the matrix
    for track in midi_file.tracks:
        track_events = []
        tons = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
        for msg in track:
            if msg.type in ('note_on', 'note_off'):
                # Extract relevant information from the message
                event_data = {
                    'type': msg.type,
                    'note': str(tons[(int(msg.note))%12]) + str(int(((int(msg.note))-(int(msg.note))%12)/12)),
                    'note': msg.note,
                    'velocity': msg.velocity,
                    'time': msg.time,
                }
                track_events.append(event_data)
        midi_matrix.append(track_events)
    print(midi_matrix)
    return midi_matrix
