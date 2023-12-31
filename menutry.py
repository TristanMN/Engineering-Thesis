from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
 
pygame.init()
display_info = pygame.display.Info()
SIZE = (display_info.current_w, display_info.current_h)
surface = pygame.display.set_mode(SIZE)
 
def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)
 
def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)
 
def options_menu():
    mainmenu._open(options)
 
 
mainmenu = pygame_menu.Menu('Welcome', SIZE[0], SIZE[1])
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Options', options_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

resolutions = [("800x600", (800, 600)), ("1024x768", (1024, 768)), ("1152x864", (1152, 864)), ("1280x600", (1280, 600)), ("1280x720", (1280, 720)), ("1280x800", (1280, 800)), ("1280x960", (1280, 960)), ("1280x1024", (1280, 1024)), ("1400x1050", (1400, 1050)), ("1440x900", (1440, 900)), ("1600x900", (1600, 900)), ("1680x1050", (1680, 1050)), ("1920x1080", (1920, 1080)), ("1920x1200", (1920, 1200)), ("2560x1080", (2560, 1080)), ("2560x1440", (2560, 1440)), ("2560x1600", (2560, 1600)), ("3440x1440", (3440, 1440)), ("3840x2160", (3840, 2160))]
options = pygame_menu.Menu('Select a Display resolution', SIZE[0], SIZE[1], theme=themes.THEME_BLUE)
options.add.selector('Display resolution :', resolutions, onchange=set_difficulty)

level = pygame_menu.Menu('Select a Difficulty', SIZE[0], SIZE[1], theme=themes.THEME_BLUE)
level.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
 
loading = pygame_menu.Menu('Loading the Game...', SIZE[0], SIZE[1], theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )
 
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))
 
update_loading = pygame.USEREVENT + 0
 
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
        if event.type == pygame.QUIT:
            exit()
 
    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())
 
    pygame.display.update()