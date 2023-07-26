import pygame
from utilities import *
import openai
import json

#This class handles all processes in the program, including the screen
#It updates the screen, draws the screen, and handles events and also maintains the clock responsible for fps
#Other classes which are processes of the program are put as parameters of this class and are updated and drawn here
class MainHandler:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 120
        self.objects = []
        self.subject_dropbox = None
        self.level_dropbox = None
        self.topic_dropbox = None

    def update(self):
        self.screen.update()
        for i in self.objects:
            i.update()

        self.topic_dropbox.update()
        self.level_dropbox.update()
        self.subject_dropbox.update()

        try:
            match self.subject_dropbox.options[self.subject_dropbox.selected]:
                case "Choose Subject...":
                    self.level_dropbox.options = ["Select subject first..."]
                    self.topic_dropbox.options = ["Select subject first..."]
                case "Science - Core":
                    self.level_dropbox.options = ["Choose Level...", "Level 1"]
                    self.topic_dropbox.options = ["Choose Topic...", "Mechanics", "Acids and Bases", "Genetic Variation"]
                case "Physics":
                    self.level_dropbox.options = ["Choose Level...", "Level 2", "Level 3"]
                    self.topic_dropbox.options = ["Choose Topic...", "Mechanics", "Waves", "Electricity"]
                case "Chemistry":
                    self.level_dropbox.options = ["Choose Level...", "Level 2", "Level 3"]
                    match self.level_dropbox.options[self.level_dropbox.selected]:
                        case "Level 2":
                            self.topic_dropbox.options = ["Choose Topic...", "Structure and Bonding", "Organics", "Chemical Reacitivty"]
                        case "Level 3":
                            self.topic_dropbox.options = ["Choose Topic...", "Thermochemistry", "Organics", "Equilibrium"]
        except Exception as e:
            print(e)

    def draw(self):
        self.screen.draw()
        for i in self.objects:
            i.draw(self.screen.screen)
        self.topic_dropbox.draw(self.screen.screen)
        self.level_dropbox.draw(self.screen.screen)
        self.subject_dropbox.draw(self.screen.screen)
        pygame.display.update()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        self.screen.events(events)
        for i in self.objects:
            i.events(events) #pass events to all objects to save a large amonut of computing power
        
        self.subject_dropbox.events(events)
        self.level_dropbox.events(events)
        self.topic_dropbox.events(events)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

    def addObject(self, obj): #Not really nessecary but makes code look nicer
        self.objects.append(obj)

    def generate(self, difficulty, question, answer, explanation, information, generation_box, answer_box):
        openai.api_key = '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'
        with open("achivement_standards.json", encoding='utf-8') as f:
            standards = json.load(f)
        fixed_context = standards[f"{self.subject_dropbox.options[self.subject_dropbox.selected]}_{self.level_dropbox.options[self.level_dropbox.selected]}_{self.topic_dropbox.options[self.topic_dropbox.selected]}"]
        if information == "Enter here...":
            information = ""
        prompt = [
            {'role': 'system', 'content': f'You are an AI tasked with generating exam questions. The subject is {self.subject_dropbox.options[self.subject_dropbox.selected]} and the topic is {self.topic_dropbox.options[self.topic_dropbox.selected]} at NCEA {self.level_dropbox.options[self.level_dropbox.selected]}. The user will provide an outline of the standard and any other additional information. Please generate a questions, {"answer, " if answer else ""} {"explanation, " if explanation else ""}on topics covered in the standard at {difficulty} level. You may create fictional scenarios to add to the question. Put Question: before the question and Answer: after the answer/explanation.'},
            {'role': 'user', 'content':f"{fixed_context}\n\nAdditional Information:\n{information}"}
        ]

        print(prompt)

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=1,
        max_tokens=1000, 
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )

        generation = response['choices'][0]['message']['content'].strip()
        print(generation)

        question = ""
        answer = ""
        toggle = False

        for line in generation.splitlines():
            if line.startswith("Question:"):
                line = line.replace("Question:", "")
                toggle = False
            if line.startswith("Answer:"):
                line = line.replace("Answer:", "")
                toggle = True

            if toggle and line.strip() != "":
                answer += line + "\n"
            else:
                question += line + "\n"

        generation_box.change_text(question)
        answer_box.change_text(answer)

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
        self.screen.fill((239, 240, 243))
        self.screen.blit(self.logo, (5, 0))
        font = pygame.font.Font("Kanit-Regular.ttf", 48)
        text = font.render("NCEA AI Q&A", True, (13, 13, 13))
        self.screen.blit(text, (115, 10 ))


if __name__ == '__main__': #Only run when ran as a script
    screen = MainScreen()
    app = MainHandler(screen)
    #test_button = BasicButton((100, 50), (100, 100), "Test", pygame.font.Font("Kanit-Regular.ttf", 24), (0, 0, 255), (0, 0, 170), None)
    #app.addObject(test_button)
    subject_dropbox = DropDown((145, 30), (15, 110), ["Choose Subject...", "Science - Core", "Physics", "Chemistry", "Statistics"], pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243))
    level_dropbox = DropDown((145, 30), (15, 150), ["Choose Level..."], pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243))
    topic_dropbox = DropDown((145, 30), (15, 190), ["Choose Topic..."], pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243))
    #topic_editbox = EditBox((145, 30), (15, 190), "Enter here...", pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), (13, 13, 13))
    diff_dropbox = DropDown((145, 30), (15, 230), ["Choose Difficulty...", "Achieved", "Merit", "Excellence"], pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243))
    text1 = SimpleText((15, 270), "Generative Options:", pygame.font.Font("Kanit-Regular.ttf", 16), (13, 13, 13))
    question_checkbox = CheckBox((30, 30), (15, 300), pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), (13, 13, 13), "Question", False)
    answer_checkbox = CheckBox((30, 30), (15, 340), pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), (13, 13, 13), "Answer", False)
    explanation_checkbox = CheckBox((30, 30), (15, 380), pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), (13, 13, 13), "Explanation", False)
    text2 = SimpleText((15, 420), "Additional Information:", pygame.font.Font("Kanit-Regular.ttf", 16), (13, 13, 13))
    text3 = SimpleText((600, 10), "Generations", pygame.font.Font("Kanit-Regular.ttf", 48), (13, 13, 13))
    text4 = SimpleText((600, 70), "Question:", pygame.font.Font("Kanit-Regular.ttf", 24), (13, 13, 13))
    question_displaybox = DisplayBox((500, 250), (600, 110), pygame.font.Font("Kanit-Regular.ttf", 12), (243, 210, 193), (13, 13, 13), (13, 13, 13), """Question goes here...""")
    text5 = SimpleText((600, 360), "Answer/Explanation:", pygame.font.Font("Kanit-Regular.ttf", 24), (13, 13, 13))
    info_editbox = EditBox((400, 200), (15, 450), "Enter here...", pygame.font.Font("Kanit-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), (13, 13, 13))
    answer_displaybox = DisplayBox((500, 250), (600, 400), pygame.font.Font("Kanit-Regular.ttf", 12), (243, 210, 193), (13, 13, 13), (13, 13, 13), "Answer goes here...")
    generate_button = BasicButton((100, 50), (15, 660), "Generate", pygame.font.Font("Kanit-Regular.ttf", 20), (255, 142, 60), (247, 131, 47), (255, 255, 254), lambda: app.generate(diff_dropbox.options[diff_dropbox.selected], question_checkbox.checked, answer_checkbox.checked, explanation_checkbox.checked, info_editbox.text, question_displaybox, answer_displaybox))
    save_button = BasicButton((100, 50), (315, 660), "Save", pygame.font.Font("Kanit-Regular.ttf", 20), (255, 142, 60), (247, 131, 47), (255, 255, 254), None)
    
    #Add in reverse order to prevent boxes from being drawn over each other
    
    #Input Side
    app.addObject(save_button)
    app.addObject(generate_button)
    app.addObject(info_editbox)
    app.addObject(text2)
    app.addObject(answer_checkbox)
    app.addObject(question_checkbox)
    app.addObject(text1)
    app.addObject(diff_dropbox)
    app.subject_dropbox = subject_dropbox
    app.level_dropbox = level_dropbox
    app.topic_dropbox = topic_dropbox

    #Generation Side
    app.addObject(answer_displaybox)
    app.addObject(question_displaybox)
    app.addObject(text3)
    app.addObject(text4)
    app.addObject(text5)
    app.addObject(explanation_checkbox)

    app.run()
    pygame.quit()