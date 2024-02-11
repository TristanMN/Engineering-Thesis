import pygame
import pygame.midi
import pygame.locals
import numpy as np
import threading
import openmidi
import fourier
import os

# colors
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
silver = (210, 210, 210)
gold = (250, 230, 150)
cyan = (0, 255, 255)
pink = (255, 0, 255)


class Graphic(object):
    def __init__(self, SIZE, file_path, player):
        pygame.init()
        display_info = pygame.display.Info()
        self.file_path = file_path
        self.SIZE = (display_info.current_w, display_info.current_h)
        self.SIZE = SIZE
        self.player = player
        self.screen = pygame.display.set_mode(self.SIZE, flags=pygame.locals.DOUBLEBUF)  # pygame.locals.FULLSCREEN |
        self.screen.fill((25, 25, 25))

    def run(self):

        def convert_song(song): # convert time in song from difference to total
            temp_time = 0
            i = 0
            for tone in song:
                temp_time += int(tone['time'])
                song[i]['time'] = temp_time
                i += 1

            temp_list = np.zeros(120, dtype=dict)  # adding duration of tone and removing ending tones
            converted_song = []
            for tone in song:
                if tone['velocity'] > 0:
                    temp_list[int(tone['note'])] = tone
                elif tone['velocity'] == 0:
                    # duration from difference of time tone_off and tone_on from temp_list
                    temp_list[int(tone['note'])]['duration'] = int(tone['time']) - int(temp_list[int(tone['note'])]['time'])
                    temp_list[int(tone['note'])]['duration_to_graphic'] = int(tone['time']) - int(
                        temp_list[int(tone['note'])]['time'])
                    temp_list[int(tone['note'])]['have_to_be_pressed'] = False
                    temp_list[int(tone['note'])]['time_to_be_pressed'] = 0
                    converted_song.append(temp_list[int(tone['note'])])
            return sorted(converted_song, key=lambda d: d['time'])

        octavs = 5
        self.width = int(self.SIZE[0] / (7 * octavs))
        print(self.width, self.SIZE[0] / (7 * octavs))

        midifile = None
        file_extension = str(self.file_path.split(".")[-1])
        # checking the need for convert by Fourier transform
        if file_extension in ['mp3', 'wav', 'flac', 'ogg', 'aac', 'wma', 'aiff', 'alac', 'dsd', 'ac3', 'amr', 'au',
                              'm4a', 'opus']:
            thread = threading.Thread(target=fourier.main(self.file_path))
            thread.start()
            thread.join()
            midifile = fourier.file

        elif file_extension == "midi":
            midifile = self.file_path

        else:
            print("Wybrano zły plik")
            return 0

        midi_matrix = openmidi.main(midifile)
        song = convert_song(midi_matrix[0])
        # song = convert_song(midi_matrix[1])
        list_of_tones = []
        list_of_playing_tones = []
        # fps_clock = pygame.time.Clock()     # game stabilisation at the expense of speed

        def key_parametres(note):   # returning window width, width, size and color of piano key
            if note % 12 == 0:  # C
                return 0, self.width, self.SIZE[1] / 4, white
            if note % 12 == 1:  # C#
                return self.width / (4 / 3), self.width / 2, self.SIZE[1] / 6, black
            if note % 12 == 2:  # D
                return self.width * 1, self.width, self.SIZE[1] / 4, white
            if note % 12 == 3:  # Eb
                return self.width / (4 / 3) + 1 * self.width, self.width / 2, self.SIZE[1] / 6, black
            if note % 12 == 4:  # E
                return self.width * 2, self.width, self.SIZE[1] / 4, white
            if note % 12 == 5:  # F
                return self.width * 3, self.width, self.SIZE[1] / 4, white
            if note % 12 == 6:  # F#
                return self.width / (4 / 3) + 3 * self.width, self.width / 2, self.SIZE[1] / 6, black
            if note % 12 == 7:  # G
                return self.width * 4, self.width, self.SIZE[1] / 4, white
            if note % 12 == 8:  # Ab
                return self.width / (4 / 3) + 4 * self.width, self.width / 2, self.SIZE[1] / 6, black
            if note % 12 == 9:  # A
                return self.width * 5, self.width, self.SIZE[1] / 4, white
            if note % 12 == 10:  # Bb
                return self.width / (4 / 3) + 5 * self.width, self.width / 2, self.SIZE[1] / 6, black
            if note % 12 == 11:  # B
                return self.width * 6, self.width, self.SIZE[1] / 4, white

        def player_info(player_name, song_name):    # checking the best score of player
            filename = str(player_name) + ".txt"
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    statistic = file.readlines()
                    info = [eval(line.strip()) for line in statistic]
                    for stats in info:
                        if stats[0] == song_name:
                            return info, stats[1]
                    return info, None

            else:
                return [], None

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', int(self.SIZE[1] / 36))
        song_name = os.path.splitext(os.path.basename(self.file_path))[0]

        player_stats, best_score = player_info(self.player, song_name)
        print(best_score, player_stats)

        combo = 0
        points = 0
        w = 0
        timesynthesia = None
        printing = False
        listblack = [0, 1, 3, 4, 5]

        # finding the connected device
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

        sizeparam = np.sqrt(self.SIZE[0] * self.SIZE[1]) / 2500     # size parameter of synthesia keys

        running = True
        while running:  # main loop
            if w == 0:
                w = 0
                for _ in range(octavs):
                    for _ in range(7):  # printing white keys of keyboard
                        pygame.draw.rect(self.screen, white,
                                         [w + 2, self.SIZE[1] - self.SIZE[1] / 4 + 2, self.width - 2, self.SIZE[1] / 4],
                                         0)
                        pygame.draw.rect(self.screen, black,
                                         [w, self.SIZE[1] - self.SIZE[1] / 4, self.width, self.SIZE[1] / 4], 2)
                        w += self.width
                w = 0
                for _ in range(octavs):  # printing black keys of keyboard
                    for n in listblack:
                        pygame.draw.rect(self.screen, black, [w + (self.width / (4 / 3)) + (n * self.width),
                                                              self.SIZE[1] - self.SIZE[1] / 4, self.width / 2,
                                                              self.SIZE[1] / 6], 0)
                    w += 7 * self.width

            note = 0
            ampli = 0
            try:
                if midi_input.poll():
                    midi_events = midi_input.read(10)
                    note = int(midi_events[0][0][1])
                    ampli = int(midi_events[0][0][2])
                    time = int(midi_events[0][1])
            except:
                pass

            if printing is False:   # loop before start
                timesynthesia = int(pygame.time.get_ticks())
                # if ampli > 0 and note not in list_of_playing_tones:
                #     list_of_playing_tones.append((note, timesynthesia))
                # if ampli == 0:
                #     list_of_playing_tones = [plays for plays in list_of_playing_tones if plays[0] != note]
                #     pygame.draw.rect(self.screen, gold,
                #                      [key_parametres(note % 12)[0] + (note - note % 12 - 36) / 12 * 7 * self.width,
                #                       self.SIZE[1] - self.SIZE[1] / 4, key_parametres(note)[1],
                #                       key_parametres(note)[2]], 0)

            if printing is True:    # loop after start
                pace = max(int(len(list_of_tones) * sizeparam), 2)  # falling speed of synthesia and accumulator
                # pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)  # black background

                # adding tone to list of displayed tones
                if len(song) > 0 and int(pygame.time.get_ticks()) - timesynthesia > song[0]['time']:
                    list_of_tones.append(song[0])
                    song.pop(0)

                # main loop of displaying tones
                for tone in list_of_tones:
                    height = min(tone['duration_to_graphic'] - 2 * tone['duration'], self.SIZE[1] - self.SIZE[1] / 4)
                    lenght = tone['duration'] / (9 / 4)
                    if self.SIZE[1] - self.SIZE[1] / 4 < lenght + height:
                        lenght = self.SIZE[1] - self.SIZE[1] / 4 - height
                        # highlighting key to press
                        pygame.draw.rect(self.screen, silver, [key_parametres(tone['note'] % 12)[0] + (
                                tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,
                                                               self.SIZE[1] - self.SIZE[1] / 4,
                                                               key_parametres(int(tone['note']))[1],
                                                               key_parametres(int(tone['note']))[2]], 10)

                    if height >= int(self.SIZE[1] - self.SIZE[1] / 4):
                        list_of_tones.remove(tone)  # removing tones after displaying

                        # building up the keyboard
                        if key_parametres(tone['note'] % 12)[3] == black:
                            pygame.draw.rect(self.screen, key_parametres(tone['note'] % 12)[3], [
                                key_parametres(tone['note'] % 12)[0] + (
                                        tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,
                                self.SIZE[1] - self.SIZE[1] / 4, key_parametres(int(tone['note']))[1],
                                key_parametres(int(tone['note']))[2]], 0)
                        else:
                            pygame.draw.rect(self.screen, white, [key_parametres(tone['note'] % 12)[0] + (
                                    tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width + 2,
                                                                  self.SIZE[1] - self.SIZE[1] / 4 + 2,
                                                                  key_parametres(int(tone['note']))[1] - 2,
                                                                  key_parametres(int(tone['note']))[2] - 2], 0)
                            pygame.draw.rect(self.screen, black, [key_parametres(tone['note'] % 12)[0] + (
                                    tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,
                                                                  self.SIZE[1] - self.SIZE[1] / 4,
                                                                  key_parametres(int(tone['note']))[1],
                                                                  key_parametres(int(tone['note']))[2]], 2)
                        if key_parametres(tone['note'] % 12 - 1)[3] == black:
                            pygame.draw.rect(self.screen, key_parametres(tone['note'] % 12 - 1)[3], [
                                key_parametres(tone['note'] % 12 - 1)[0] + (
                                        tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,
                                self.SIZE[1] - self.SIZE[1] / 4, key_parametres(int(tone['note'] - 1))[1],
                                key_parametres(int(tone['note'] - 1))[2]], 0)
                        if key_parametres(tone['note'] % 12 + 1)[3] == black:
                            pygame.draw.rect(self.screen, key_parametres(tone['note'] % 12 + 1)[3], [
                                key_parametres(tone['note'] % 12 + 1)[0] + (
                                        tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,
                                self.SIZE[1] - self.SIZE[1] / 4, key_parametres(int(tone['note'] + 1))[1],
                                key_parametres(int(tone['note'] + 1))[2]], 0)

                    # ploting synthesia
                    pygame.draw.rect(self.screen, cyan, [key_parametres(tone['note'] % 12)[0] + (
                            tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, height,
                                                         key_parametres(int(tone['note']))[1], lenght], 10)
                    pygame.draw.rect(self.screen, (25, 25, 25), [key_parametres(tone['note'] % 12)[0] + (
                            tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, height - pace * 2,
                                                                 key_parametres(int(tone['note']))[1], pace * 2], 0)
                    pygame.draw.rect(self.screen, (25, 25, 25), [key_parametres(tone['note'] % 12)[0] + (
                            tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width + 10,
                                                                 height + lenght - 10 - pace * 2,
                                                                 key_parametres(int(tone['note']))[1] - 20, pace * 2], 0)

                    # pygame.draw.rect(self.screen, pink, [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, height + lenght, key_parametres(int(tone['note']))[1], pace], 10)
                    # pygame.draw.rect(self.screen, (25, 25, 25), [key_parametres(tone['note'] % 12)[0] + (tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width, height - pace, key_parametres(int(tone['note']))[1], pace], 0)

                    # collecting points
                    if lenght + height + 40 < self.SIZE[1] - self.SIZE[1] / 4 < lenght + height + 40 + pace:
                        tone['have_to_be_pressed'] = True
                        tone['time_to_be_pressed'] = tone['duration_to_graphic']

                    # checking keystrokes
                    if tone['have_to_be_pressed'] is True and tone['note'] == note and (tone['velocity'] > 0 and ampli > 0):  # sprawdzanie kliknięcia | zapisywanie klawisza do listy i szukanie po liście zgadzającego się i pop z listy, jeśli nie ma lub jest inny kliknięty reset combo
                        tone['have_to_be_pressed'] = False
                        combo += 1
                        points += 10 * combo    # add points after good pressed
                        # highlight the good pressed key
                        pygame.draw.rect(self.screen, gold, [key_parametres(tone['note'] % 12)[0] + (
                                tone['note'] - tone['note'] % 12 - 36) / 12 * 7 * self.width,
                                                             self.SIZE[1] - self.SIZE[1] / 4,
                                                             key_parametres(int(tone['note']))[1],
                                                             key_parametres(int(tone['note']))[2]], 0)
                        pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[1] / 4, int(self.SIZE[1] / 12)], 0)

                        print(tone['have_to_be_pressed'], tone['note'], note, tone['velocity'], ampli, "COMBO: ", combo,
                              "POINTS: ", points)

                    # reset combo after bad pressed or no pressed
                    elif tone['have_to_be_pressed'] is True and 250 + pace > (
                            tone['duration_to_graphic'] - tone['time_to_be_pressed']) >= 250:
                        combo = 0
                        tone['have_to_be_pressed'] = False
                        pygame.draw.rect(self.screen, (25, 25, 25),
                                         [0, int(self.SIZE[1] / 24), self.SIZE[1] / 4, int(self.SIZE[1] / 24)], 0)
                        print(tone['have_to_be_pressed'], tone['note'], note, tone['velocity'], ampli, "COMBO: ", combo,
                              "POINTS: ", points)
                    # elif tone['note'] != note and ampli > 0:
                    #     combo = 0
                    #     pygame.draw.rect(self.screen, (25, 25, 25), [0, int(self.SIZE[1] / 24), self.SIZE[1] / 4, int(self.SIZE[1] / 24)], 0)

                    tone['duration_to_graphic'] += pace
                    pygame.display.flip()

                if len(list_of_tones) == 0 and len(song) == 0:
                    printing = False

                # displaying points
                text_surface = font.render('Best score: ' + str(best_score), True, (255, 255, 255))
                self.screen.blit(text_surface, (self.SIZE[0] - self.SIZE[1] / 4, 0))
                text_surface = font.render('Points: ' + str(points), True, (255, 255, 255))
                self.screen.blit(text_surface, (0, 0))
                text_surface = font.render('Combo: ' + str(combo), True, (255, 255, 255))
                self.screen.blit(text_surface, (0, int(self.SIZE[1] / 24)))

            # keys functionality
            for event in pygame.event.get():  # start-space quit-esc
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # save player statistics
                    if best_score:
                        if points > best_score:
                            print(player_stats)
                            for n, stats in enumerate(player_stats):
                                if stats[0] == song_name:
                                    player_stats[n] = (song_name, points)
                    else:
                        player_stats.append((song_name, points))
                    with open((str(self.player) + ".txt"), 'w') as file:
                        for stats in player_stats:
                            file.write(f'({repr(stats[0])}, {stats[1]})\n')
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    printing = True
            # fps_clock.tick(15)
            pygame.display.update()

        pygame.time.wait(10)
        pygame.midi.quit()

# TESTS
# (3440,1440) (1920,1080) (800,600)
# begin = Graphic((3440,1440),r"E:\Studia\PRACA INZYNIERSKA\Engineering-Thesis\A Great Big World Christina Aguilera - Say Something_conv.midi")
# begin.run()
# pygame.draw.rect(window, color, [window_width, window_height, weight, height], filling)
