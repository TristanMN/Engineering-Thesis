#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from midi2audio import FluidSynth

audio_path = os.path.join(r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis")
#audio_file = audio_path + "\\output.midi"
audio_file = audio_path + "\\fourier.midi"
# Ścieżka do pliku MIDI
input_midi = audio_file

# Ścieżka do pliku MP3 (po konwersji)
#output_mp3 = audio_path + "\\output.mp3"
output_mp3 = audio_path + "\\fourier.mp3"



# Inicjalizacja obiektu FluidSynth
fluidsynth = os.path.join(r"C:\fluidsynthx64\bin\fluidsynth.exe")
soundfont_file = "C:\ProgramData\soundfonts\Roland SC-55.sf2"
#soundfont_file = "C:\ProgramData\soundfonts\Gabe the Dog.sf2"
#soundfont_file = "C:\ProgramData\soundfonts\Super Mario Bros..sf2"
fs = FluidSynth(soundfont_file)

# Konwersja pliku MIDI na MP3
fs.midi_to_audio(input_midi, output_mp3)