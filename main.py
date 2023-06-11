import pygame
from buttons import BasicButton

#This class handles all processes in the program, including the screen
#It updates the screen, draws the screen, and handles events and also maintains the clock responsible for fps
#Other classes which are processes of the program are put as parameters of this class and are updated and drawn here
class MainHandler:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.objects = []

    def update(self):
        self.screen.update()
        for i in self.objects:
            i.update()

    def draw(self):
        self.screen.draw()
        for i in self.objects:
            i.draw(self.screen.screen)
        pygame.display.update()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        self.screen.events(events)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

    def addObject(self, obj):
        self.objects.append(obj)

#This class is the screen of the program
#It is responsible for drawing the screen and handling events
#The logo and title are part of the screen and drawn here
class MainScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.logo = pygame.image.load("logo.png")
        self.logo = pygame.transform.scale(self.logo, (100, 100))
        pygame.display.set_caption("NCEA AI")

    def events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.logo, (5, 0))
        font = pygame.font.Font("Kanit-Regular.ttf", 48)
        text = font.render("NCEA AI Q&A", True, (0, 0, 0))
        self.screen.blit(text, (115, 10 ))


if __name__ == '__main__':
    screen = MainScreen()
    app = MainHandler(screen)
    app.run()
    pygame.quit()