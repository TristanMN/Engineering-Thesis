import pygame
pygame.init()

RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
SIZE = (3440,1380)
screen = pygame.display.set_mode(SIZE)
screen.fill(WHITE)
pygame.draw.rect(screen, (25, 25, 25), [0, 0, SIZE[0], SIZE[1]-SIZE[1]/4], 0)
octavs = 5
w = 0
width = int(SIZE[0]/(7*octavs))
print(width, SIZE[0]/(7*octavs))
while True:
    pygame.draw.rect(screen, (25, 25, 25), [0, 0, SIZE[0], SIZE[1] - SIZE[1] / 4], 0)       #czarne tło
    for i in range(octavs):     #czarne klawisze
        pygame.draw.rect(screen, BLACK, [w+(width/(4/3)), SIZE[1]-SIZE[1]/4, width/2, SIZE[1]/6], 0)
        pygame.draw.rect(screen, BLACK, [w+(width/(4/3))+(1*width), SIZE[1]-SIZE[1]/4, width/2, SIZE[1]/6], 0)
        pygame.draw.rect(screen, BLACK, [w+(width/(4/3))+(3*width), SIZE[1]-SIZE[1]/4, width/2, SIZE[1]/6], 0)
        pygame.draw.rect(screen, BLACK, [w+(width/(4/3))+(4*width), SIZE[1]-SIZE[1]/4, width/2, SIZE[1]/6], 0)
        pygame.draw.rect(screen, BLACK, [w+(width/(4/3))+(5*width), SIZE[1]-SIZE[1]/4, width/2, SIZE[1]/6], 0)
        for o in range(7):      #białe klawisze
            pygame.draw.rect(screen, BLACK, [w, SIZE[1]-SIZE[1]/4, width, SIZE[1]/4], 2)
            w += width
    timestart = min(int(pygame.time.get_ticks() / 4), int(SIZE[1] - SIZE[1] / 4))       #lecące klawisze
    timestop = max(int(pygame.time.get_ticks() / 4)-200, 0)
    print(timestart, timestop)
    pygame.draw.rect(screen, BLUE, [(width/(4/3))+(18*width), timestop, width/2, timestart-timestop], 0)
    pygame.draw.rect(screen, BLUE, [(width/(4/3))+(21*width), timestop-50, width/2, timestart-timestop+50], 0)
    pygame.draw.rect(screen, BLUE, [(width/(4/3))+(25*width), timestop-100, width/2, timestart-timestop+100], 0)
    pygame.display.update()
pygame.time.wait(2000)
pygame.quit()
#pygame.draw.rect(okno, kolor, [szerokość_okna, wysokość_okna, szerokość, wysokość], wypełnienie)