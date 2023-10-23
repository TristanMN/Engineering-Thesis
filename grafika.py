import pygame, sys
import numpy as np
from openmidi import main

pygame.init()

red = (255,0,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)

class Graphic(object):
    def __init__(self):
        display_info = pygame.display.Info()
        self.SIZE = (display_info.current_w, display_info.current_h)
        self.screen = pygame.display.set_mode(self.SIZE)
        self.screen.fill((25, 25, 25))

    def run(self):
        def convert_song(song):
            temp_time = 0   #convert time in song from difference to total
            i = 0
            for tone in song:
                temp_time += int(tone['time'])
                song[i]['time'] = temp_time
                i += 1

            temp_list = np.zeros(144, dtype=dict)   #adding duration of tone and delete offing tones
            converted_song = []
            for tone in song:
                if tone['velocity'] > 0:
                    temp_list[int(tone['note'])] = tone
                elif tone['velocity'] == 0:
                    temp_list[int(tone['note'])]['duration'] = int(tone['time']) - int(temp_list[int(tone['note'])]['time'])   #duration from difference of time tone off and tone on from temp_list
                    temp_list[int(tone['note'])]['duration_to_graphic'] = int(tone['time']) - int(temp_list[int(tone['note'])]['time'])
                    converted_song.append(temp_list[int(tone['note'])])
            return sorted(converted_song, key=lambda d: d['time'])

#stworzyć listę po której będzie ciągle wyświetlało klawisze dodając tony po czasie i sprawdzająć przy okazji na boku czy element powinien zostać usunięty z listy gdy wyjdzie poza ekran

#                pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)   ##############



        octavs = 5
        self.width = int(self.SIZE[0]/(7*octavs))
        print(self.width, self.SIZE[0]/(7*octavs))
        w = 0
        timestop = 0
        time = 0
        timesynthesia = None
        printing = False
        midi_matrix = main()

        song = convert_song(midi_matrix[0])
        list_of_tones = []
#        song = convert_song(midi_matrix[1])

        def key_width(note):
            if note%12 == 0:    #C
                return 0, self.width
            if note%12 == 1:    #C#
                return self.width/(4/3), self.width/2
            if note%12 == 2:    #D
                return self.width * 1, self.width
            if note%12 == 3:    #Eb
                return self.width/(4/3)+1*self.width, self.width/2
            if note%12 == 4:    #E
                return self.width * 2, self.width
            if note%12 == 5:    #F
                return self.width * 3, self.width
            if note%12 == 6:    #F#
                return self.width/(4/3)+3*self.width, self.width/2
            if note%12 == 7:    #G
                return self.width * 4, self.width
            if note%12 == 8:    #Ab
                return self.width/(4/3)+4*self.width, self.width/2
            if note%12 == 9:    #A
                return self.width * 5, self.width
            if note%12 == 10:   #Bb
                return self.width/(4/3)+5*self.width, self.width/2
            if note%12 == 11:   #B
                return self.width * 6, self.width

        while True:
#            pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)       #czarne tło
            w = 0
            for i in range(octavs):     #czarne klawisze
                for o in range(7):      #białe klawisze
                    pygame.draw.rect(self.screen, white, [w + 2, self.SIZE[1]-self.SIZE[1]/4 + 2, self.width  - 2, self.SIZE[1]/4], 0)
                    pygame.draw.rect(self.screen, black, [w, self.SIZE[1]-self.SIZE[1]/4, self.width, self.SIZE[1]/4], 2)
                    w += self.width
            w = 0
            for i in range(octavs):  # czarne klawisze
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3)), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3))+(1*self.width), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3))+(3*self.width), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3))+(4*self.width), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3))+(5*self.width), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                for o in range(7):
                    w += self.width

            if printing is False:
                timesynthesia = int(pygame.time.get_ticks())
            if printing is True:
                pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)  # czarne tło
                if len(song) > 0 and int(pygame.time.get_ticks()) - timesynthesia > song[0]['time']:
                    list_of_tones.append(song[0])
                    song.pop(0)
                for tone in list_of_tones:
                    height = min(tone['duration_to_graphic'] - 2*tone['duration'], self.SIZE[1]-self.SIZE[1]/4)
                    lenght = tone['duration'] / (5/4)
                    if self.SIZE[1]-self.SIZE[1]/4 < lenght + height:
                        lenght = self.SIZE[1] - self.SIZE[1] / 4 - height
                    if height == int(self.SIZE[1]-self.SIZE[1]/4):
                        list_of_tones.remove(tone)
                    pygame.draw.rect(self.screen, blue, [key_width(tone['note']%12)[0] + (tone['note'] - tone['note']%12 -36)/12 * 7 * self.width, height, key_width(int(tone['note']))[1], lenght], 0)
                    tone['duration_to_graphic'] += 10
                    pygame.display.update()


            for event in pygame.event.get():    #wychodzenie esc #włączanie synthesi spacją
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    printing = True

            pygame.display.update()

        pygame.time.wait(10)



begin = Graphic()
begin.run()
#pygame.draw.rect(okno, kolor, [szerokość_okna, wysokość_okna, szerokość, wysokość], wypełnienie)