import pygame

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
        octavs = 5
        w = 0
        width = int(self.SIZE[0]/(7*octavs))
        print(width, self.SIZE[0]/(7*octavs))
        timestop = 0
        while timestop < 100:
            pygame.draw.rect(self.screen, (25, 25, 25), [0, 0, self.SIZE[0], self.SIZE[1] - self.SIZE[1] / 4], 0)       #czarne tło
            for i in range(octavs):     #czarne klawisze
                pygame.draw.rect(self.screen, black, [w+(width/(4/3)), self.SIZE[1]-self.SIZE[1]/4, width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(width/(4/3))+(1*width), self.SIZE[1]-self.SIZE[1]/4, width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(width/(4/3))+(3*width), self.SIZE[1]-self.SIZE[1]/4, width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(width/(4/3))+(4*width), self.SIZE[1]-self.SIZE[1]/4, width/2, self.SIZE[1]/6], 0)
                pygame.draw.rect(self.screen, black, [w+(width/(4/3))+(5*width), self.SIZE[1]-self.SIZE[1]/4, width/2, self.SIZE[1]/6], 0)
                for o in range(7):      #białe klawisze
                    pygame.draw.rect(self.screen, black, [w, self.SIZE[1]-self.SIZE[1]/4, width, self.SIZE[1]/4], 2)
                    w += width
            timestart = min(int(pygame.time.get_ticks() / 4), int(self.SIZE[1] - self.SIZE[1] / 4))       #lecące klawisze
            timestop = max(int(pygame.time.get_ticks() / 4)-200, 0)
            print(timestart, timestop)
            pygame.draw.rect(self.screen, blue, [(width/(4/3))+(18*width), timestop, width/2, timestart-timestop], 0)
            pygame.draw.rect(self.screen, blue, [(width/(4/3))+(21*width), timestop-50, width/2, timestart-timestop+50], 0)
            pygame.draw.rect(self.screen, blue, [(width/(4/3))+(25*width), timestop-100, width/2, timestart-timestop+100], 0)
            pygame.display.update()
        pygame.time.wait(10)
        pygame.quit()

#        def key(self):
#            pass

begin = Graphic()
begin.run()
#SIZE = (3440,1380)
#pygame.draw.rect(okno, kolor, [szerokość_okna, wysokość_okna, szerokość, wysokość], wypełnienie)