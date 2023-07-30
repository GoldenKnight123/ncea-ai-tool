import pygame
from utilities import *
import openai
import json
import threading
import datetime

# This class handles all processes in the program, including the screen
# It updates the screen, draws the screen, and handles events and also maintains the clock responsible for fps
# Other classes which are processes of the program are put as parameters of this class and are updated and drawn here
class MainHandler:
    def __init__(self, screen):
        self.screen = screen  # The screen is the main screen of the program
        self.running = True  # The running variable is used to stop the program
        self.clock = pygame.time.Clock()  # The clock is used to maintain the fps
        self.fps = 120  # The fps is the amount of times the screen is updated per second
        self.objects = []  # The objects list is used to store all objects which are updated and drawn
        self.subject_dropbox = None  # The subject dropbox is used to select the subject
        self.level_dropbox = None  # The level dropbox is used to select the level
        self.topic_dropbox = None  # The topic dropbox is used to select the topic
        self.answer_checkbox = None  # The answer checkbox is used to select whether the answer is shown or not
        self.response = None  # The response is the response from the openai api
        self.info_text = SimpleText((120, 680), "", pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (255, 0, 0))  # The info text is used to display information to the user
        self.dropdown_opened = False  # The dropdown opened variable is used to check if a dropdown is opened or not

    def update(self):
        # Update the screen and all objects
        self.screen.update()
        for i in self.objects:
            i.update()

        self.topic_dropbox.update()
        self.level_dropbox.update()
        self.subject_dropbox.update()

        # Update the options of the level and topic dropboxes based on the subject dropbox
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
        except:
            pass

    def draw(self):
        # Draw the screen and all objects
        self.screen.draw()
        for i in self.objects:
            i.draw(self.screen.screen)
        self.topic_dropbox.draw(self.screen.screen)
        self.level_dropbox.draw(self.screen.screen)
        self.subject_dropbox.draw(self.screen.screen)
        self.info_text.draw(self.screen.screen)

        try:
            if self.answer_checkbox.checked == False:
                answer_box = pygame.Rect(600, 405, 500, 245)
                pygame.draw.rect(self.screen.screen, (239, 240, 243), answer_box, border_radius=5)
                pygame.draw.rect(self.screen.screen, (13, 13, 13), answer_box, 2, border_radius=5)
        except:
            pass
        pygame.display.update()

    def events(self):
        # Handle all events such as key presses and mouse clicks
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.events(events)
        for i in self.objects:
            i.events(events)  # pass events to all objects to save a large amonut of computing power
        
        self.subject_dropbox.events(events)
        self.level_dropbox.events(events)
        self.topic_dropbox.events(events)

    def run(self):
        # While loop which runs the program
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

    def addObject(self, obj):  # Not really nessecary but makes code look nicer
        self.objects.append(obj)

    def make_request(self, prompt):
        # Make a request to the openai api
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )

        self.response = response
    
    def generate(self, difficulty, information, generation_box, answer_box):
        # Generate a question and answer based on the user's input
        # First the api key is set
        openai.api_key = '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'
        
        # Load the standards from the json file
        with open("achivement_standards.json", encoding='utf-8') as f:
            standards = json.load(f)

        # Attempt to get the standard from the json file
        try:
            fixed_context = standards[f"{self.subject_dropbox.options[self.subject_dropbox.selected]}_{self.level_dropbox.options[self.level_dropbox.selected]}_{self.topic_dropbox.options[self.topic_dropbox.selected]}"]
        # If the standard is not found, then we tell the user to select all options as if all options are selected then the standard will be found
        except:
            # Show error message
            self.info_text.text = "Please select more information"
            return
        
        # Remove any error messages
        self.info_text.text = ""
        
        # Join the information into a string
        information = " ".join(information)

        # If the information is the default text, then we set it to none
        if information == "Enter here...":
            information = "None."

        # If the difficulty is the default text, then we set it to any level of difficulty
        if difficulty == "Any difficulty":
            difficulty = "any level of difficulty"

        # Load the prompt into the correct format
        prompt = [
            {'role': 'system', 'content': f'You are an AI tasked with generating exam questions. The subject is {self.subject_dropbox.options[self.subject_dropbox.selected]} and the topic is {self.topic_dropbox.options[self.topic_dropbox.selected]} at NCEA {self.level_dropbox.options[self.level_dropbox.selected]}. The user will provide an outline of the standard and any other additional information. Please generate a question and answer with explanation on topics covered in the standard at {difficulty} level. You may create fictional scenarios to add to the question. Put Question: before the question and Answer: after the answer/explanation.'},
            {'role': 'user', 'content': f"{fixed_context}\n\nAdditional Information:\n{information}"}
        ]

        # Start a thread to make the request
        api_thread = threading.Thread(target=self.make_request, args=(prompt,))
        api_thread.start()

        # Using a timer and a text variable, we display "Generating..." on the screen while the api is generating
        # This text will be animate to show everything is working and the program is not frozen
        timer = 0  
        text = 'Generating...' 
        
        # While we have not recieved a response from the api, we display "Generating..."
        while self.response is None:
            if timer >= 120:
                timer = 0
            elif timer >= 90:
                text = 'Generating..'
            elif timer >= 60:
                text = 'Generating.'
            elif timer >= 30:
                text = 'Generating'
            else:
                text = 'Generating...'

            timer += 1
            
            # Update the screen
            generation_box.change_text(text)
            answer_box.change_text(text)
            self.events()
            self.update()
            self.screen.draw()
            for i in self.objects:
                i.draw(self.screen.screen)
            self.topic_dropbox.draw(self.screen.screen)
            self.level_dropbox.draw(self.screen.screen)
            self.subject_dropbox.draw(self.screen.screen)

            # Draw a box in the center of the screen
            generating_box = pygame.Rect(440, 260, 400, 200)
            pygame.draw.rect(self.screen.screen, (239, 240, 243), generating_box)
            pygame.draw.rect(self.screen.screen, (13, 13, 13), generating_box, 5)

            # Draw cancel button, if it's hovered over then change colour
            cancel_button = pygame.Rect(740, 400, 90, 50)
            if cancel_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen.screen, (247, 131, 47), cancel_button)
            else:
                pygame.draw.rect(self.screen.screen, (255, 142, 60), cancel_button)
            pygame.draw.rect(self.screen.screen, (247, 131, 47), cancel_button, 5)

            # Draw cancel text
            cancel_text = pygame.font.Font("RobotoCondensed-Regular.ttf", 24).render("Cancel", True, (255, 255, 254))
            cancel_text_rect = cancel_text.get_rect(center=(785, 425))
            self.screen.screen.blit(cancel_text, cancel_text_rect)

            # if user clicks cancel button, stop generating
            mouse_pos = pygame.mouse.get_pos()
            if cancel_button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.response = None
                    question_displaybox.change_text("Question goes here...")
                    answer_displaybox.change_text("Answer goes here...")
                    del api_thread
                    break

            # Draw the "Generating..." text inside the box
            text_surface = pygame.font.Font("RobotoCondensed-Regular.ttf", 36).render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(640, 360))
            self.screen.screen.blit(text_surface, text_rect)
            pygame.display.update()
            self.clock.tick(self.fps)

        # If the response is None (cancelled), then we don't do anything
        if self.response == None:
            return
        
        # Join the thread back to the main thread
        api_thread.join()

        # Get text from the response
        generation = self.response['choices'][0]['message']['content'].strip()

        # Process each line of the response to get the question and answer        
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
            elif line.strip() != "":
                question += line + "\n"

        # Change the text of the display boxes to the question and answer
        generation_box.change_text(question)
        answer_box.change_text(answer)
        self.response = None

    def save(self, question_displaybox, answer_displaybox):
        # Save the question and answer to a file
        # The file is named as the current date and time
        # The file is saved into a folder called "Saved Questions"\
        # The file is saved as a .txt file

        # First we check if the question and answer are the default text, if yes then we don't save
        if question_displaybox.text == ["Question goes here..."] or answer_displaybox.text == ["Answer goes here..."]:
            self.info_text.text = "Please generate a question first"
            return

        # Get the current date and time
        now = datetime.datetime.now()

        # Format the date and time into a string
        date = now.strftime("%Y-%m-%d %H-%M-%S")

        # Save the question and answer to a file
        with open(f"Saved Questions/{date}.txt", "w", encoding='utf-8') as f:
            f.write("Question:\n" + '\n'.join(question_displaybox.text) + "\n\n" + "Answer:\n" + '\n'.join(answer_displaybox.text))
            f.close()
        self.info_text.text = "Saved Successfully"

# This class is the screen of the program
# It is responsible for drawing the screen and handling events
# The logo and title are part of the screen and drawn here
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
        font = pygame.font.Font("RobotoCondensed-Regular.ttf", 48)
        text = font.render("NCEA AI Q&A", True, (13, 13, 13))
        self.screen.blit(text, (115, 10))


if __name__ == '__main__': # Only run when ran as a script
    screen = MainScreen()
    app = MainHandler(screen)
    
    # Create all components on the GUI

    # Input side
    subject_dropbox = DropDown((145, 30), (15, 110), ["Choose Subject...", "Science - Core", "Physics", "Chemistry"], pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), app)
    level_dropbox = DropDown((145, 30), (15, 150), ["Choose Level..."], pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), app)
    topic_dropbox = DropDown((145, 30), (15, 190), ["Choose Topic..."], pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), app)
    diff_dropbox = DropDown((145, 30), (15, 230), ["Any difficulty", "Achieved", "Merit", "Excellence"], pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), app)
    text1 = SimpleText((15, 270), "Generative Options:", pygame.font.Font("RobotoCondensed-Regular.ttf", 16), (13, 13, 13))
    answer_checkbox = CheckBox((30, 30), (15, 300), pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), (13, 13, 13), "Show Answer", False)
    text2 = SimpleText((15, 340), "Additional Information:", pygame.font.Font("RobotoCondensed-Regular.ttf", 16), (13, 13, 13))
    info_editbox = EditBox((400, 280), (15, 370), "Enter here...", pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (255, 255, 254), (13, 13, 13), (239, 240, 243), (13, 13, 13))
    generate_button = BasicButton((100, 50), (15, 660), "Generate", pygame.font.Font("RobotoCondensed-Regular.ttf", 20), (255, 142, 60), (247, 131, 47), (255, 255, 254), lambda: app.generate(diff_dropbox.options[diff_dropbox.selected], info_editbox.text, question_displaybox, answer_displaybox))
    save_button = BasicButton((100, 50), (315, 660), "Save", pygame.font.Font("RobotoCondensed-Regular.ttf", 20), (255, 142, 60), (247, 131, 47), (255, 255, 254), lambda: app.save(question_displaybox, answer_displaybox))
    
    # Output side
    text3 = SimpleText((600, 10), "Generations", pygame.font.Font("RobotoCondensed-Regular.ttf", 48), (13, 13, 13))
    text4 = SimpleText((600, 70), "Question:", pygame.font.Font("RobotoCondensed-Regular.ttf", 24), (13, 13, 13))
    question_displaybox = DisplayBox((500, 245), (600, 110), pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (243, 210, 193), (13, 13, 13), (13, 13, 13), """Question goes here...""")
    text5 = SimpleText((600, 365), "Answer/Explanation:", pygame.font.Font("RobotoCondensed-Regular.ttf", 24), (13, 13, 13))
    answer_displaybox = DisplayBox((500, 245), (600, 405), pygame.font.Font("RobotoCondensed-Regular.ttf", 12), (243, 210, 193), (13, 13, 13), (13, 13, 13), "Answer goes here...")
    
    # Add all components to the app
    # Added in reverse order to prevent boxes from being drawn over each other
    
    # Input Side
    app.addObject(save_button)
    app.addObject(generate_button)
    app.addObject(info_editbox)
    app.addObject(text2)
    app.addObject(answer_checkbox)
    app.addObject(text1)
    app.addObject(diff_dropbox)
    app.subject_dropbox = subject_dropbox
    app.level_dropbox = level_dropbox
    app.topic_dropbox = topic_dropbox
    app.answer_checkbox = answer_checkbox

    # Generation Side
    app.addObject(answer_displaybox)
    app.addObject(question_displaybox)
    app.addObject(text3)
    app.addObject(text4)
    app.addObject(text5)

    # Run the app, and quit pygame when done
    app.run()
    pygame.quit()
