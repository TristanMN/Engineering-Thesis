import pygame
import pygame.midi
import pygame.locals
import numpy as np
import threading
import openmidi
import fouriertry

red = (255,0,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
silver = (210,210,210)
gold = (250,230,150)
green = (0,255,255)

class Graphic(object):
    def __init__(self, SIZE, file_path):
        pygame.init()
        display_info = pygame.display.Info()
        self.file_path = file_path
        self.SIZE = (display_info.current_w, display_info.current_h)
        self.SIZE = SIZE
        self.screen = pygame.display.set_mode(self.SIZE, flags = pygame.locals.DOUBLEBUF) #pygame.locals.FULLSCREEN |
        self.screen.fill((25, 25, 25))

    def run(self):
        def convert_song(song):
            temp_time = 0   #convert time in song from difference to total
            i = 0
            for tone in song:
                temp_time += int(tone['time'])
                song[i]['time'] = temp_time
                i += 1

            temp_list = np.zeros(120, dtype=dict)   #adding duration of tone and delete offing tones
            converted_song = []
            for tone in song:
                if tone['velocity'] > 0:
                    temp_list[int(tone['note'])] = tone
                elif tone['velocity'] == 0:
                    temp_list[int(tone['note'])]['duration'] = int(tone['time']) - int(temp_list[int(tone['note'])]['time'])   #duration from difference of time tone off and tone on from temp_list
                    temp_list[int(tone['note'])]['duration_to_graphic'] = int(tone['time']) - int(temp_list[int(tone['note'])]['time'])
                    temp_list[int(tone['note'])]['have_to_be_pressed'] = False
                    temp_list[int(tone['note'])]['time_to_be_pressed'] = 0
                    converted_song.append(temp_list[int(tone['note'])])
            return sorted(converted_song, key=lambda d: d['time'])

#stworzyć listę po której będzie ciągle wyświetlało klawisze dodając tony po czasie i sprawdzająć przy okazji na boku czy element powinien zostać usunięty z listy gdy wyjdzie poza ekran

#                pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)   ##############

        octavs = 5
        self.width = int(self.SIZE[0]/(7*octavs))
        print(self.width, self.SIZE[0]/(7*octavs))

        midifile = None
        file_extension = str(self.file_path.split(".")[-1])

        if file_extension in ['mp3', 'wav', 'flac', 'ogg', 'aac', 'wma', 'aiff', 'alac', 'dsd','ac3', 'amr', 'au', 'm4a', 'opus']:
            thread = threading.Thread(target=fouriertry.main(self.file_path))
            thread.start()
            thread.join()
            midifile = fouriertry.file

        elif file_extension == "midi":
            midifile = self.file_path
        else:
            print("Wybrano zły plik")
            return 0
        midi_matrix = openmidi.main(midifile)
        song = convert_song(midi_matrix[0])
        #song = convert_song(midi_matrix[1])
        list_of_tones = []
        list_of_playing_tones = []
        fps_clock = pygame.time.Clock()


        def key_parametres(note):
            if note%12 == 0:    #C
                return 0, self.width, self.SIZE[1]/4, white
            if note%12 == 1:    #C#
                return self.width/(4/3), self.width/2, self.SIZE[1]/6, black
            if note%12 == 2:    #D
                return self.width * 1, self.width, self.SIZE[1]/4, white
            if note%12 == 3:    #Eb
                return self.width/(4/3)+1*self.width, self.width/2, self.SIZE[1]/6, black
            if note%12 == 4:    #E
                return self.width * 2, self.width, self.SIZE[1]/4, white
            if note%12 == 5:    #F
                return self.width * 3, self.width, self.SIZE[1]/4, white
            if note%12 == 6:    #F#
                return self.width/(4/3)+3*self.width, self.width/2, self.SIZE[1]/6, black
            if note%12 == 7:    #G
                return self.width * 4, self.width, self.SIZE[1]/4, white
            if note%12 == 8:    #Ab
                return self.width/(4/3)+4*self.width, self.width/2, self.SIZE[1]/6, black
            if note%12 == 9:    #A
                return self.width * 5, self.width, self.SIZE[1]/4, white
            if note%12 == 10:   #Bb
                return self.width/(4/3)+5*self.width, self.width/2, self.SIZE[1]/6, black
            if note%12 == 11:   #B
                return self.width * 6, self.width, self.SIZE[1]/4, white

        
        combo = 0
        points = 0
        w = 0
        timesynthesia = None
        printing = False
        listblack = [0,1,3,4,5]

        pygame.midi.init()
        print("MIDI Input Devices:")
        input_device_id = None
        for i in range(pygame.midi.get_count()):
            print(i)
            device_info = pygame.midi.get_device_info(i)
            print(device_info)
            if device_info[2]:
                print(f"{i}: {device_info[1].decode()}")
                if input_device_id is None:
                    input_device_id = i
        global midi_input
        midi_input = None
        if input_device_id is not None:
            print(input_device_id)
            midi_input = pygame.midi.Input(input_device_id)
            print(f"Receiving MIDI input from {pygame.midi.get_device_info(input_device_id)[1].decode()}")
        else:
            print("No valid MIDI input devices found.")
            pygame.midi.quit()

        pace = 10
        running = True
        while running:     #główna pętla
            if w == 0:
                w = 0
                for _ in range(octavs):
                    for _ in range(7):      #białe klawisze
                        pygame.draw.rect(self.screen, white, [w + 2, self.SIZE[1]-self.SIZE[1]/4 + 2, self.width  - 2, self.SIZE[1]/4], 0)
                        pygame.draw.rect(self.screen, black, [w, self.SIZE[1]-self.SIZE[1]/4, self.width, self.SIZE[1]/4], 2)
                        w += self.width
                w = 0
                for _ in range(octavs):     #czarne klawisze
                    for n in listblack:
                        pygame.draw.rect(self.screen, black, [w + (self.width / (4 / 3)) + (n * self.width), self.SIZE[1] - self.SIZE[1] / 4, self.width / 2, self.SIZE[1]/6], 0)
                    w += 7*self.width

            note = 0
            ampli = 0
            try:
                #if midi_input:
                if midi_input.poll():
                    midi_events = midi_input.read(10)
                    note = int(midi_events[0][0][1])
                    ampli = int(midi_events[0][0][2])
                    time = int(midi_events[0][1])
            except:
                pass

            if printing is False:
                timesynthesia = int(pygame.time.get_ticks())
                #podświetlanie trafionego klawisza
                if ampli > 0 and note not in list_of_playing_tones:
                    list_of_playing_tones.append((note, timesynthesia))
                if ampli == 0 and note in list_of_playing_tones:
                    #list_of_playing_tones.remove((note, ))
                    pygame.draw.rect(self.screen, gold, [key_parametres(note % 12)[0] + (note - note % 12 - 36) / 12 * 7 * self.width,self.SIZE[1] - self.SIZE[1] / 4,key_parametres(note)[1],key_parametres(note)[2]], 0)
            if printing is True:
                # pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)  # czarne tło
                if len(song) > 0 and int(pygame.time.get_ticks()) - timesynthesia > song[0]['time']:
                    list_of_tones.append(song[0])
                    song.pop(0)
                for tone in list_of_tones:
                    height = min(tone['duration_to_graphic'] - 2*tone['duration'], self.SIZE[1]-self.SIZE[1]/4)
                    lenght = tone['duration'] / (5/4)
                    if self.SIZE[1]-self.SIZE[1]/4 < lenght + height:
                        lenght = self.SIZE[1] - self.SIZE[1] / 4 - height
                    #podświetlanie klawisza który powinno się nacisnąć
                        pygame.draw.rect(self.screen, silver, [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,self.SIZE[1] - self.SIZE[1] / 4,key_parametres(int(tone['note']))[1],key_parametres(int(tone['note']))[2]], 10)
                    if height >= int(self.SIZE[1]-self.SIZE[1]/4):
                        list_of_tones.remove(tone)
                    #nadbudowywanie klawiatury
                        if key_parametres(tone['note'] % 12)[3] == black:
                            pygame.draw.rect(self.screen, key_parametres(tone['note'] % 12)[3], [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, self.SIZE[1] - self.SIZE[1] / 4, key_parametres(int(tone['note']))[1], key_parametres(int(tone['note']))[2]], 0)
                        else:
                            pygame.draw.rect(self.screen, white, [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width +2, self.SIZE[1] - self.SIZE[1] / 4 + 2, key_parametres(int(tone['note']))[1] - 2,key_parametres(int(tone['note']))[2] - 2], 0)
                            pygame.draw.rect(self.screen, black, [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,self.SIZE[1] - self.SIZE[1] / 4, key_parametres(int(tone['note']))[1],key_parametres(int(tone['note']))[2]], 2)
                        if key_parametres(tone['note'] % 12 - 1)[3] == black:
                            pygame.draw.rect(self.screen, key_parametres(tone['note'] % 12 - 1)[3], [key_parametres(tone['note'] % 12 - 1)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, self.SIZE[1] - self.SIZE[1] / 4, key_parametres(int(tone['note'] - 1))[1], key_parametres(int(tone['note'] - 1))[2]], 0)
                        if key_parametres(tone['note'] % 12 + 1)[3] == black:
                            pygame.draw.rect(self.screen, key_parametres(tone['note'] % 12 + 1)[3], [key_parametres(tone['note'] % 12 + 1)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, self.SIZE[1] - self.SIZE[1] / 4, key_parametres(int(tone['note'] + 1))[1], key_parametres(int(tone['note'] + 1))[2]], 0)
                    #rysowanie synthesi
                    pygame.draw.rect(self.screen, green, [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, height, key_parametres(int(tone['note']))[1], lenght], 10)
                    pygame.draw.rect(self.screen, (25, 25, 25), [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, height - pace, key_parametres(int(tone['note']))[1], pace], 0)
                    pygame.draw.rect(self.screen, (25, 25, 25), [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width + 10, height + lenght - 10 - pace, key_parametres(int(tone['note']))[1] - 20, pace], 0)

                    #pygame.draw.rect(self.screen, silver, [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, height + lenght, key_parametres(int(tone['note']))[1], pace], 10)
                    #pygame.draw.rect(self.screen, (25, 25, 25), [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, height - pace, key_parametres(int(tone['note']))[1], pace], 0)

                    #collecting points
                    if lenght + height + 40 < self.SIZE[1]-self.SIZE[1]/4 < lenght + height + 40 + pace:
                        tone['have_to_be_pressed'] = True
                        tone['time_to_be_pressed'] = tone['duration_to_graphic']
                    if tone['have_to_be_pressed'] is True and tone['note'] == note and ((tone['velocity'] > 0 and ampli > 0) or (tone['velocity'] == 0 and ampli == 0)):    #sprawdzanie kliknięcia | zapisywanie klawisza do listy i szukanie po liście zgadzającego się i pop z listy, jeśli nie ma lub jest inny kliknięty reset combo
                        tone['have_to_be_pressed'] = False
                        combo += 1
                        points = 10 * combo + points
                        #podświetlanie trafionego klawisza
                        pygame.draw.rect(self.screen, gold, [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,self.SIZE[1] - self.SIZE[1] / 4,key_parametres(int(tone['note']))[1],key_parametres(int(tone['note']))[2]], 0)

                        print(tone['have_to_be_pressed'],tone['note'], note, tone['velocity'], ampli, "COMBO: ", combo, "POINTS: ", points)
                    if tone['have_to_be_pressed'] == True and 250 + pace > (tone['duration_to_graphic'] - tone['time_to_be_pressed']) > 250:
                        combo = 0
                        tone['have_to_be_pressed'] = False
                        print(tone['have_to_be_pressed'],tone['note'], note, tone['velocity'], ampli, "COMBO: ", combo, "POINTS: ", points)

                    tone['duration_to_graphic'] += pace
                    pygame.display.flip()
                    
                if len(list_of_tones) == 0 and len(song) == 0:
                    printing = False


            for event in pygame.event.get():    #wychodzenie esc #włączanie synthesi spacją
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    printing = True
            #fps_clock.tick(15)
            pygame.display.update()

        pygame.time.wait(10)
        pygame.midi.quit()


# begin = Graphic()
# begin.run()
#pygame.draw.rect(okno, kolor, [szerokość_okna, wysokość_okna, szerokość, wysokość], wypełnienie)