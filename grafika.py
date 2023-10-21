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
        self.screen.fill(white)


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
                    converted_song.append(temp_list[int(tone['note'])])
            return sorted(converted_song, key=lambda d: d['time'])

#stworzyć listę po której będzie ciągle wyświetlało klawisze dodając tony po czasie i sprawdzająć przy okazji na boku czy element powinien zostać usunięty z listy gdy wyjdzie poza ekran
        def key(self, note, time, duration):
            timestop = 0
            temptime = pygame.time.get_ticks()
            while timestop < self.SIZE[1] - self.SIZE[1]/4 - duration:
                timestart = min(int(pygame.time.get_ticks()), int(self.SIZE[1] - self.SIZE[1] / 4))  # lecące klawisze
                timestop = max(int(pygame.time.get_ticks()) - temptime, 0)

                pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)   ##############

                pygame.draw.rect(self.screen, blue, [int(note/2-18) * self.width, timestop, self.width,  int(duration)], 0)     #szerokość do zmiany
                pygame.display.update()

        octavs = 5
        self.width = int(self.SIZE[0]/(7*octavs))
        print(self.width, self.SIZE[0]/(7*octavs))
        w = 0
        timestop = 0
        time = 0
        temptime = None
        printing = False
        midi_matrix = main()

        song = convert_song(midi_matrix[0])
#        song = convert_song(midi_matrix[1])


        while timestop < 1000:
            if printing is False:
                temptime = int(pygame.time.get_ticks())
            if printing is True:
                if int(pygame.time.get_ticks()) - temptime > song[0]['time']:
                    print(song[0])
                    key(self, note = song[0]['note'], time = song[0]['time'], duration = song[0]['duration'])
                    song.pop(0)

            pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)       #czarne tło
            for i in range(octavs):     #czarne klawisze
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3)), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3))+(1*self.width), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3))+(3*self.width), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3))+(4*self.width), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(self.width/(4/3))+(5*self.width), self.SIZE[1]-self.SIZE[1]/4, self.width/2, self.SIZE[1]/6], 0)
                for o in range(7):      #białe klawisze
                    pygame.draw.rect(self.screen, black, [w, self.SIZE[1]-self.SIZE[1]/4, self.width, self.SIZE[1]/4], 2)
                    w += self.width

            for event in pygame.event.get():    #wychodzenie esc
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    printing = True


            # for keys in midi_matrix[1]:
            #     if keys['type'] == 'note_on' and keys['velocity'] > 0:
            #         time += keys['time']
            #         key(self, note = int(keys['note']), time = time)

            pygame.display.update()

        pygame.time.wait(10)



begin = Graphic()
begin.run()
#pygame.draw.rect(okno, kolor, [szerokość_okna, wysokość_okna, szerokość, wysokość], wypełnienie)