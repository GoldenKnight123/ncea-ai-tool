import pygame
from utilities import *

#This class handles all processes in the program, including the screen
#It updates the screen, draws the screen, and handles events and also maintains the clock responsible for fps
#Other classes which are processes of the program are put as parameters of this class and are updated and drawn here
class MainHandler:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 240
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
        for i in self.objects:
            i.events(events) #pass events to all objects to save a large amonut of computing power

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

    def addObject(self, obj): #Not really nessecary but makes code look nicer
        self.objects.append(obj)

#This class is the screen of the program
#It is responsible for drawing the screen and handling events
#The logo and title are part of the screen and drawn here
class MainScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
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


if __name__ == '__main__': #Only run when ran as a script
    screen = MainScreen()
    app = MainHandler(screen)
    #test_button = BasicButton((100, 50), (100, 100), "Test", pygame.font.Font("Kanit-Regular.ttf", 24), (0, 0, 255), (0, 0, 170), None)
    #app.addObject(test_button)
    subject_dropbox = DropDown((145, 30), (15, 110), ["Choose Subject...", "Physics", "Chemistry"], pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (100, 100, 100))
    level_dropbox = DropDown((145, 30), (15, 150), ["Choose Level...", "Level 1", "Level 2", "Level 3"], pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (100, 100, 100))
    topic_editbox = EditBox((145, 30), (15, 190), "Enter Topic...", pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (100, 100, 100), (0, 0, 0), 25)
    diff_dropbox = DropDown((145, 30), (15, 230), ["Choose Difficulty...", "Achieved", "Merit", "Excellence"], pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (100, 100, 100))
    text1 = SimpleText((15, 270), "Generative Options:", pygame.font.Font("Kanit-Regular.ttf", 16), (0, 0, 0))
    question_checkbox = CheckBox((30, 30), (15, 300), pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (100, 100, 100), (0, 0, 0), "Question", False)
    answer_checkbox = CheckBox((30, 30), (15, 340), pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (100, 100, 100), (0, 0, 0), "Answer", False)
    explanation_checkbox = CheckBox((30, 30), (15, 380), pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (100, 100, 100), (0, 0, 0), "Explanation", False)
    text2 = SimpleText((600, 10), "Generations", pygame.font.Font("Kanit-Regular.ttf", 48), (0, 0, 0))
    text3 = SimpleText((600, 70), "Question:", pygame.font.Font("Kanit-Regular.ttf", 24), (0, 0, 0))
    question_displaybox = DisplayBox((500, 250), (600, 110), pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (0, 0, 0), """Question goes here...""")
    text4 = SimpleText((600, 360), "Answer/Explanation::", pygame.font.Font("Kanit-Regular.ttf", 24), (0, 0, 0))
    answer_displaybox = DisplayBox((500, 250), (600, 400), pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 255), (192, 192, 192), (0, 0, 0), "Answer goes here...")
    generate_button = BasicButton((100, 50), (15, 500), "Generate", pygame.font.Font("Kanit-Regular.ttf", 20), (192, 192, 192), (100, 100, 100), None)
    save_button = BasicButton((100, 50), (15, 560), "Save", pygame.font.Font("Kanit-Regular.ttf", 20), (192, 192, 192), (100, 100, 100), None)
    
    #Add in reverse order to prevent boxes from being drawn over each other
    
    #Input Side
    app.addObject(save_button)
    app.addObject(generate_button)
    app.addObject(answer_checkbox)
    app.addObject(question_checkbox)
    app.addObject(text1)
    app.addObject(diff_dropbox)
    app.addObject(topic_editbox)
    app.addObject(level_dropbox)
    app.addObject(subject_dropbox)

    #Generation Side
    app.addObject(answer_displaybox)
    app.addObject(question_displaybox)
    app.addObject(text2)
    app.addObject(text3)
    app.addObject(text4)
    app.addObject(explanation_checkbox)

    app.run()
    pygame.quit()