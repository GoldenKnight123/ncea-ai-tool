import pygame

#Basic button class
#size: tuple (width, height)
#pos: tuple (x, y)
#colours: tuple (R, G, B)
class BasicButton:
    def __init__(self, size, pos, text, font, colour, hover_colour, function):
        self.size = size #tuple
        self.pos = pos #tuple
        self.text = text
        self.font = font
        self.colour = colour
        self.hover_colour = hover_colour
        self.function = function
        self.hovered = False
        self.clicked = False #Used to check if the button was clicked in the current frame

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        #Check if mouse is hovering over button
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
            self.hovered = True
            #Check if mouse is clicking on button
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True #Set clicked to true so that the button can't be clicked multiple times with one click
                if self.function != None:
                    self.function()
        else:
            self.hovered = False

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        
    def draw(self, screen):
        #Draw different colour if hovered
        if self.hovered:
            pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=10)
        else:
            pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=10)
        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)
        screen.blit(text, text_rect)

        #Draw border if clicked
        if self.clicked:
            pygame.draw.rect(screen, (255, 255, 255), (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=10)
        
    def events(self, events):
        pass

#Dropdown menu class  
class DropDown:
    def __init__(self, size, pos, options, font, colour, border_color, hover_colour):
        self.size = size #tuple
        self.pos = pos #tuple
        self.options = options
        self.font = font
        self.colour = colour
        self.border_color = border_color
        self.hover_colour = hover_colour
        self.hovered = False
        self.hover_selection = 0
        self.clicked = False
        self.selected = 0
        self.open = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        #Check if mouse is hovering over button
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
            self.hovered = True
            #Check if mouse is clicking on button
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True #Set clicked to true so that the button can't be clicked multiple times with one click
                self.open = not self.open

        else:
            self.hovered = False

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        
        if self.open:
            for i in range(len(self.options)):
                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] + (i + 1) * self.size[1] < mouse_pos[1] < self.pos[1] + (i + 2) * self.size[1]:
                    self.hover_selection = i
                    #Check if mouse is clicking on button
                    if pygame.mouse.get_pressed()[0] and not self.clicked:
                        self.clicked = True
                        self.selected = i
                        self.open = False

                if not pygame.mouse.get_pressed()[0]:
                    self.clicked = False

    def draw(self, screen):
        #Draw different colour if hovered or open
        if self.hovered or self.open:
            pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2)
        else:
            pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2)
        text = self.font.render(self.options[self.selected], True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.left = self.pos[0] + 10 #Pad text from left
        text_rect.centery = self.pos[1] + self.size[1] / 2
        screen.blit(text, text_rect)

        #Draw options if open
        if self.open:
            for i in range(len(self.options)):
                #Draw different colour if the option is hovered
                if self.hover_selection == i:
                    pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1] + (i + 1) * self.size[1], self.size[0], self.size[1]))
                    pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1] + (i + 1) * self.size[1], self.size[0], self.size[1]), 2)
                else:
                    pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1] + (i + 1) * self.size[1], self.size[0], self.size[1]))
                    pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1] + (i + 1) * self.size[1], self.size[0], self.size[1]), 2)
                text = self.font.render(self.options[i], True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.left = self.pos[0] + 10 #Pad text from left
                text_rect.centery = self.pos[1] + (i + 1) * self.size[1] + self.size[1] / 2
                screen.blit(text, text_rect)

        #Built in arrow on the right
        pygame.draw.polygon(screen, (0, 0, 0), ((self.pos[0] + self.size[0] - 20, self.pos[1] + 20), (self.pos[0] + self.size[0] - 10, self.pos[1] + 20), (self.pos[0] + self.size[0] - 15, self.pos[1] + 30)))

    def events(self, events):
        pass

#Editbox class
class EditBox:
    def __init__(self, size, pos, default_text, font, colour, border_colour, hover_colour, text_colour, max_length):
        self.size = size
        self.pos = pos
        self.text = default_text
        self.font = font #Font may need to be changed to a monospace font to prevent text from going outside of box
        self.colour = colour
        self.border_colour = border_colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.max_length = max_length
        self.hovered = False
        self.clicked = False
        self.selected = False
        self.selected_display_timer = 100
        self.backspace_hold_timer = 0

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        #Check if mouse is hovering over editbox
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
            self.hovered = True
            #Check if mouse is clicking on editbox
            if pygame.mouse.get_pressed()[0] and not self.selected and not self.clicked:
                self.clicked = True
                self.selected = True
        else:
            self.hovered = False
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.selected = False

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        #Once the backspace key is held/pressed, a timer is started
        if self.backspace_hold_timer > 0:
            self.backspace_hold_timer += 1
            #If the timer is greater than 30, the last character is removed
            #The timer is reset to 27 to allow more frames between each character removal
            if self.backspace_hold_timer > 30:
                self.backspace_hold_timer = 27
                self.text = self.text[:-1]
    
    def draw(self, screen):
        #Draw different colour if hovered
        if self.hovered or self.selected:
            pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            pygame.draw.rect(screen, self.border_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2)
        else:
            pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            pygame.draw.rect(screen, self.border_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2)

        #If the object is selected, display a blinking _ at the end of the text to indicate it is selected and being edited
        if self.selected:
            #The blinking is controlled by a timer with 2 phases to reduce having to use another variable
            if self.selected_display_timer <= 50 and self.selected_display_timer > 0:
                self.selected_display_timer -= 1
                text = self.font.render(self.text + "_", True, self.text_colour)
            elif self.selected_display_timer <= 0:
                self.selected_display_timer = 100
                text = self.font.render(self.text, True, self.text_colour)
            else:
                self.selected_display_timer -= 1
                text = self.font.render(self.text, True, self.text_colour)
        else:
            text = self.font.render(self.text, True, self.text_colour)
        
        text_rect = text.get_rect()
        text_rect.left = self.pos[0] + 10

        #Pad text from left
        text_rect.centery = self.pos[1] + self.size[1] / 2
        screen.blit(text, text_rect)

    def events(self, events):
        #While the editbox is selected, it will accept keyboard input
        if self.selected:
            for event in events:
                #Any key that is pressed will be added to the text
                #If it is backspace, the last character will be removed
                #Timer is used to allow holding backspace to delete multiple characters
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                        self.backspace_hold_timer += 1 #Once the timer is greater than 0 it will be incremented until it reaches 30, done by the update() function
                    elif event.key == pygame.K_RETURN:
                        self.selected = False
                    elif len(self.text) < self.max_length:
                        self.text += event.unicode

                #Once the backspace key is released, the timer is reset
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_hold_timer = 0