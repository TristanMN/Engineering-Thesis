import pygame
import pygame_menu
from pygame_menu import themes
import threading
import tkinter as tk
from tkinter import filedialog
import grafika

pygame.init()
display_info = pygame.display.Info()
SIZE = (display_info.current_w, display_info.current_h)


def main():
    running = True
    global SIZE
    global DIFF
    surface = pygame.display.set_mode(SIZE)

    def set_difficulty(value, difficulty):
        global DIFF
        DIFF = difficulty

    def synthesia(path):  # start graphic
        begin = grafika.Graphic(SIZE, path, player.get_value())
        thread = threading.Thread(target=begin.run())
        thread.start()
        thread.join()

    def start_the_game():  # selecting the file
        root = tk.Tk()
        root.withdraw()
        file_path = tk.filedialog.askopenfilename()
        root.quit()
        synthesia(file_path)

    def options_menu():
        mainmenu._open(options)

    def exit_menu():
        running = False
        pygame.quit()
        exit()

    def set_resolution(resolution, value):
        global SIZE
        SIZE = value

    mainmenu = pygame_menu.Menu('Chopin Fighter', SIZE[0], SIZE[1])
    # menu buttons
    player = mainmenu.add.text_input('Name: ', default='Player')
    mainmenu.add.button('Play', start_the_game)
    mainmenu.add.button('Options', options_menu)
    mainmenu.add.button('Quit', exit_menu)

    resolutions = [("Default", (display_info.current_w, display_info.current_h)), ("800x600", (800, 600)),
                   ("1024x768", (1024, 768)), ("1152x864", (1152, 864)), ("1280x600", (1280, 600)),
                   ("1280x720", (1280, 720)), ("1280x800", (1280, 800)), ("1280x960", (1280, 960)),
                   ("1280x1024", (1280, 1024)), ("1400x1050", (1400, 1050)), ("1440x900", (1440, 900)),
                   ("1600x900", (1600, 900)), ("1680x1050", (1680, 1050)), ("1920x1080", (1920, 1080)),
                   ("1920x1200", (1920, 1200)), ("2560x1080", (2560, 1080)), ("2560x1440", (2560, 1440)),
                   ("2560x1600", (2560, 1600)), ("3440x1440", (3440, 1440)), ("3840x2160", (3840, 2160))]

    options = pygame_menu.Menu('Options', SIZE[0], SIZE[1], theme=themes.THEME_BLUE)
    options.add.button('Set', main)
    options.add.selector('Display resolution :', resolutions, onchange=set_resolution)
    options.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty)

    arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

    while running:
        events = pygame.event.get()
        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if mainmenu.get_current().get_selected_widget():
                arrow.draw(surface, mainmenu.get_current().get_selected_widget())

        pygame.display.update()


main()
