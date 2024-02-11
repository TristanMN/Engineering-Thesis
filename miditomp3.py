#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from midi2audio import FluidSynth

# path to song
audio_path = os.path.join(r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis\widma")
file = "\\Rufus Wainwright - Hallelujah_conv2"
audio_file = audio_path + file + ".midi"

# path to mp3 file
output_mp3 = audio_path + file + ".mp3"

# FluidSynth init
fluidsynth = os.path.join(r"C:\fluidsynthx64\bin\fluidsynth.exe")
soundfont_file = "C:\ProgramData\soundfonts\Roland SC-55.sf2"
fs = FluidSynth(soundfont_file)

# conversion
fs.midi_to_audio(input_midi, output_mp3)
