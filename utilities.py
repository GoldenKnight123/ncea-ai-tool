import pygame

# Basic button class
# size: tuple (width, height)
# pos: tuple (x, y)
# colours: tuple (R, G, B)
class BasicButton:
    def __init__(self, size, pos, text, font, colour, hover_colour, text_colour, function):
        self.size = size # tuple
        self.pos = pos # tuple
        self.text = text
        self.font = font
        self.colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.function = function
        self.hovered = False
        self.clicked = False # Used to check if the button was clicked in the current frame

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        # Check if mouse is hovering over button
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
            self.hovered = True
            # Check if mouse is clicking on button
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True # Set clicked to true so that the button can't be clicked multiple times with one click
                if self.function != None:
                    self.function()
        else:
            self.hovered = False

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        
    def draw(self, screen):
        # Draw different colour if hovered
        if self.hovered:
            pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=10)
        else:
            pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=10)
        text = self.font.render(self.text, True, self.text_colour)
        text_rect = text.get_rect()
        text_rect.center = (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)
        screen.blit(text, text_rect)

        # Draw border if clicked
        if self.clicked:
            pygame.draw.rect(screen, (255, 255, 255), (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=10)
        
    def events(self, events):
        pass

# Dropdown menu class  
class DropDown:
    def __init__(self, size, pos, options, font, colour, border_color, hover_colour, app):
        self.size = size # tuple
        self.pos = pos # tuple
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
        self.app = app

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        # Check if mouse is hovering over button
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
            self.hovered = True
            # Check if mouse is clicking on button
            if pygame.mouse.get_pressed()[0] and not self.clicked and not self.app.dropdown_opened:
                self.clicked = True # Set clicked to true so that the button can't be clicked multiple times with one click
                self.open = True
                self.app.dropdown_opened = True

            elif pygame.mouse.get_pressed()[0] and not self.clicked and self.app.dropdown_opened:
                self.clicked = True
                self.open = False
                self.app.dropdown_opened = False
            
            elif not pygame.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False

        else:
            self.hovered = False
        
        # If the dropdown is open, check if the mouse is hovering over any of the options
        if self.open:
            for i in range(len(self.options)):
                if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] + (i + 1) * self.size[1] < mouse_pos[1] < self.pos[1] + (i + 2) * self.size[1]:
                    self.hover_selection = i
                    # Check if mouse is clicking on button
                    if pygame.mouse.get_pressed()[0] and not self.clicked:
                        self.clicked = True
                        self.selected = i
                        self.open = False
                        self.app.dropdown_opened = False
                        
                    if not pygame.mouse.get_pressed()[0] and self.clicked:
                        self.clicked = False

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def draw(self, screen):
        # Draw different colour if hovered or open
        if self.hovered or self.open:
            pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=5)
            pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=5)
        else:
            pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=5)
            pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=5)
        try:
            text = self.font.render(self.options[self.selected], True, (0, 0, 0))
        except IndexError:
            self.selected = 0
            text = self.font.render(self.options[self.selected], True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.left = self.pos[0] + 10 # Pad text from left
        text_rect.centery = self.pos[1] + self.size[1] / 2
        screen.blit(text, text_rect)

        # Draw options if open
        if self.open:
            for i in range(len(self.options)):
                # Draw different colour if the option is hovered
                if self.hover_selection == i:
                    pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1] + (i + 1) * self.size[1], self.size[0], self.size[1]))
                    pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1] + (i + 1) * self.size[1], self.size[0], self.size[1]), 2)
                else:
                    pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1] + (i + 1) * self.size[1], self.size[0], self.size[1]))
                    pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1] + (i + 1) * self.size[1], self.size[0], self.size[1]), 2)
                text = self.font.render(self.options[i], True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.left = self.pos[0] + 10 # Pad text from left
                text_rect.centery = self.pos[1] + (i + 1) * self.size[1] + self.size[1] / 2
                screen.blit(text, text_rect)

        # Built in arrow on the right pointing down that scales with the size of the dropdown
        pygame.draw.polygon(screen, (0, 0, 0), ((self.pos[0] + self.size[0] - self.size[0]/7.5, self.pos[1] + self.size[1]*0.4), (self.pos[0] + self.size[0] - self.size[0]/15, self.pos[1] + self.size[1]*0.4), (self.pos[0] + self.size[0] - self.size[0]/10, self.pos[1] + self.size[1]*0.4 + self.size[1]/5)))

    def events(self, events):
        pass


# Editbox class
class EditBox:
    def __init__(self, size, pos, default_text, font, colour, border_colour, hover_colour, text_colour):
        self.size = size
        self.pos = pos
        self.font = font
        self.colour = colour
        self.border_colour = border_colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.hovered = False
        self.clicked = False
        self.selected = False
        self.selected_display_timer = 100
        self.backspace_hold_timer = 0

        # Process each letter in the text and split it into lines if it is too long
        self.text = []
        temp_word = ""
        temp_text = ""
        for i in range(len(default_text)):
            if default_text[i] == " ":
                if self.font.size(temp_text + temp_word + " ")[0] >= self.size[0] - 20:
                    self.text.append(temp_text)
                    temp_text = temp_word
                    temp_word = ""
                else:
                    temp_text += temp_word
                    temp_word = ""
            if default_text[i] == "\n":
                if self.font.size(temp_text + temp_word)[0] >= self.size[0] - 20:
                    self.text.append(temp_text)
                    temp_text = ""
                    temp_word = ""
                else:
                    self.text.append(temp_text + temp_word)
                    temp_text = "" 
                    temp_word = ""
            else:
                temp_word += default_text[i]
        temp_text += temp_word
        self.text.append(temp_text)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        # Check if mouse is hovering over editbox
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
            self.hovered = True
            # Check if mouse is clicking on editbox
            if pygame.mouse.get_pressed()[0] and not self.selected and not self.clicked:
                self.clicked = True
                self.selected = True
                if self.text[0] == "Enter here..." and len(self.text) == 1:
                    self.text[0] = ""
        else:
            self.hovered = False
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.selected = False
                if self.text[0] == "" and len(self.text) == 1:
                    self.text[0] = "Enter here..."

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        # Once the backspace key is held/pressed, a timer is started
        if self.backspace_hold_timer > 0:
            self.backspace_hold_timer += 1
            # If the timer is greater than 30, the last character is removed
            # The timer is reset to 27 to allow more frames between each character removal
            if self.backspace_hold_timer > 30:
                self.backspace_hold_timer = 27
                for i in range(len(self.text), 0, -1):
                    if len(self.text[i-1]) > 0:
                        self.text[i-1] = self.text[i-1][:-1]
                        if len(self.text[i-1]) <= 0 and i > 1:
                            self.text.pop(i-1)
                        break
    
    def draw(self, screen):
        # Draw different colour if hovered
        if self.hovered or self.selected:
            pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=5)
            pygame.draw.rect(screen, self.border_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=5)
        else:
            pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=5)
            pygame.draw.rect(screen, self.border_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=5)

        for i in range(len(self.text)):
            # If the object is selected, display a blinking _ at the end of the text to indicate it is selected and being edited
            if self.selected and i == len(self.text) - 1:
                # The blinking is controlled by a timer with 2 phases to reduce having to use another variable
                if self.selected_display_timer <= 50 and self.selected_display_timer > 0:
                    self.selected_display_timer -= 1
                    text = self.font.render(self.text[i] + "_", True, self.text_colour)
                elif self.selected_display_timer <= 0:
                    self.selected_display_timer = 100
                    text = self.font.render(self.text[i], True, self.text_colour)
                else:
                    self.selected_display_timer -= 1
                    text = self.font.render(self.text[i], True, self.text_colour)
            else:
                text = self.font.render(self.text[i], True, self.text_colour)
            
            text_rect = text.get_rect()
            text_rect.left = self.pos[0] + 10

            # Pad text from left
            text_rect.centery = self.pos[1] + self.size[1] / 2
            text_rect.top = self.pos[1] + (i + 1) * self.font.size(self.text[i])[1] - self.font.size(self.text[i])[1] + 5
            screen.blit(text, text_rect)
        
    def events(self, events):
        # While the editbox is selected, it will accept keyboard input
        if self.selected:
            for event in events:
                # Any key that is pressed will be added to the text
                # If it is backspace, the last character will be removed
                # Timer is used to allow holding backspace to delete multiple characters
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        for i in range(len(self.text), 0, -1):
                            if len(self.text[i-1]) > 0:
                                self.text[i-1] = self.text[i-1][:-1]
                                if len(self.text[i-1]) <= 0 and i > 1:
                                    self.text.pop(i-1)
                                break
                        self.backspace_hold_timer += 1 # Once the timer is greater than 0 it will be incremented until it reaches 30, done by the update() function
                    elif event.key == pygame.K_RETURN:
                        self.selected = False
                    elif self.font.size(self.text[-1] + event.unicode)[0] >= self.size[0] - 20:
                        # If there is enough vertical space
                        if self.font.size(" ")[1] * len(self.text) < self.size[1] - 20:
                            self.text.append(event.unicode)
                    else:
                        self.text[-1] += event.unicode

                # Once the backspace key is released, the timer is reset
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_hold_timer = 0
                        

# Checkbox class
class CheckBox:
    def __init__(self, size, pos, font, colour, border_colour, hover_colour, text_colour, text, checked):
        self.size = size
        self.pos = pos
        self.font = font
        self.colour = colour
        self.border_colour = border_colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.text = text
        self.checked = checked
        self.hovered = False
        self.clicked = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        # Check if mouse is hovering over checkbox
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
            self.hovered = True
            # Check if mouse is clicking on checkbox
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.checked = not self.checked
        else:
            self.hovered = False

        if pygame.mouse.get_pressed()[0]:
            self.clicked = True
        else:
            self.clicked = False
            
    def draw(self, screen):
        # Draw different colour if hovered
        if self.hovered:
            pygame.draw.rect(screen, self.hover_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=5)
            pygame.draw.rect(screen, self.border_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=5)
        else:
            pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=5)
            pygame.draw.rect(screen, self.border_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=5)

        # Draw a check if checked, consists of 2 lines
        if self.checked:
            pygame.draw.line(screen, self.text_colour, (self.pos[0] + self.size[0]/4, self.pos[1] + self.size[1]/2), (self.pos[0] + self.size[0]/3, self.pos[1] + self.size[1]*0.75), 3)
            pygame.draw.line(screen, self.text_colour, (self.pos[0] + self.size[0]/3, self.pos[1] + self.size[1]*0.75), (self.pos[0] + self.size[0]*0.75, self.pos[1] + self.size[1]/4), 3)

        text = self.font.render(self.text, True, self.text_colour)
        text_rect = text.get_rect()
        text_rect.left = self.pos[0] + self.size[0] + 10
        text_rect.centery = self.pos[1] + self.size[1] / 2
        screen.blit(text, text_rect)
    
    def events(self, events):
        pass

# Static text display class
class SimpleText:
    def __init__(self, pos, text, font, colour):
        self.pos = pos
        self.text = text
        self.font = font
        self.colour = colour

    def update(self):
        pass

    def draw(self, screen):
        # Draw text into screen
        text = self.font.render(self.text, True, self.colour)
        text_rect = text.get_rect()
        text_rect.left = self.pos[0]
        text_rect.top = self.pos[1]

        screen.blit(text, text_rect)

    def events(self, events):
        pass

# Large text display box class
class DisplayBox:
    def __init__(self, size, pos, font, colour, border_colour, text_colour, text):
        self.size = size
        self.pos = pos
        self.font = font
        self.colour = colour
        self.border_colour = border_colour
        # No hover color as it is not interactable and the user can only scroll through it
        self.text_colour = text_colour
        
        # Parse text into lines
        self.text = []
        temp_word = ""
        temp_text = ""
        for i in range(len(text)):
            if text[i] == " ":
                if self.font.size(temp_text + temp_word + " ")[0] >= self.size[0] - 20:
                    self.text.append(temp_text)
                    temp_text = temp_word
                    temp_word = ""
                else:
                    temp_text += temp_word
                    temp_word = ""
            if text[i] == "\n":
                if self.font.size(temp_text + temp_word)[0] >= self.size[0] - 20:
                    self.text.append(temp_text)
                    temp_text = ""
                    temp_word = ""
                else:
                    self.text.append(temp_text + temp_word)
                    temp_text = "" 
                    temp_word = ""
            else:
                temp_word += text[i]
        temp_text += temp_word
        self.text.append(temp_text)
        self.clicked = False
        self.scroll_lock = False
        self.scroll = 0
        
        # If the length of the text is greater than the size of the box, the user can scroll through it, else the scroll bar is disabled and not drawn
        # The max scroll value is the length of the text minus the size of the box
        if len(self.text) * self.font.size(self.text[0])[1] > self.size[1]:
            self.max_scroll = (len(self.text) + 1) * self.font.size(self.text[0])[1] - self.size[1]
        else:
            self.max_scroll = -1

    def update(self):
        # If mouse is hovered over scroll bar, the user can slide it up and down to control the scroll
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] + self.size[0] - 20 < mouse_pos[0] < self.pos[0] + self.size[0] + 20 and self.pos[1] - 20 < mouse_pos[1] < self.pos[1] + self.size[1] + 20:
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.scroll_lock = True
                self.scroll = (mouse_pos[1] - self.pos[1] - 6) / (self.size[1] - 14) * self.max_scroll

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
            self.scroll_lock = False

        if pygame.mouse.get_pressed()[0]:
            self.clicked = True

        if self.scroll_lock:
            self.scroll = (mouse_pos[1] - self.pos[1] - 6) / (self.size[1] - 14) * self.max_scroll
        
        # Clamp scroll value
        if self.scroll < 0:
            self.scroll = 0
        if self.scroll > self.max_scroll:
            self.scroll = self.max_scroll

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), border_radius=5)
        # If text is outside of the box, it isn't drawn
        # If it is partially outside of the box, it is cut off
        for i in range(len(self.text)):
            top = self.pos[1] + (i + 1) * self.font.size(self.text[i])[1] - self.scroll - 10
            if top > self.pos[1] - self.font.size(self.text[i])[1] and top < self.pos[1] + self.size[1]:
                text = self.font.render(self.text[i], True, self.text_colour)
                text_rect = text.get_rect()
                text_rect.left = self.pos[0] + 10
                text_rect.top = top

                screen.blit(text, text_rect)

            elif top < self.pos[1] - self.font.size(self.text[i])[1] and top + self.font.size(self.text[i])[1] > self.pos[1] - self.font.size(self.text[i])[1]:
                text = self.font.render(self.text[i], True, self.text_colour)
                text_rect = text.get_rect()
                text_rect.left = self.pos[0] + 10
                text_rect.top = top

                screen.blit(text, text_rect)

            elif top > self.pos[1] + self.size[1] + self.font.size(self.text[i])[1] and top + self.font.size(self.text[i])[1] < self.pos[1] + self.size[1]:
                text = self.font.render(self.text[i], True, self.text_colour)
                text_rect = text.get_rect()
                text_rect.left = self.pos[0] + 10
                text_rect.top = top

                screen.blit(text, text_rect)

        # White boxes to cover up the text that is outside of the box
        pygame.draw.rect(screen, (239, 240, 243), (self.pos[0], self.pos[1]-30, self.size[0], 30), border_radius=5)
        pygame.draw.rect(screen, (239, 240, 243), (self.pos[0], self.pos[1]+self.size[1], self.size[0], 30), border_radius=5)
        pygame.draw.rect(screen, self.border_colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]), 2, border_radius=5)

        # Draw a scroll bar on the side which is a gray dot that moves if scrolling is needed
        if self.max_scroll != -1:
            pygame.draw.circle(screen, (192, 192, 192), (self.pos[0] + self.size[0] - 6, self.pos[1] + 6 + (self.size[1]-11)*self.scroll/self.max_scroll), 5)

    def events(self, events):
        # If the mouse wheel is scrolled, the scroll value is changed
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1] + self.size[1]:
            for event in events:
                if event.type == pygame.MOUSEWHEEL:
                    self.scroll -= event.y * 10

    def change_text(self, text):
        # Split text into lines based on the width of the box
        self.text = []
        temp_word = ""
        temp_text = ""
        for i in range(len(text)):
            if text[i] == " ":
                if self.font.size(temp_text + temp_word + " ")[0] >= self.size[0] - 20:
                    self.text.append(temp_text)
                    temp_text = temp_word
                    temp_word = ""
                else:
                    temp_text += temp_word
                    temp_word = ""
            if text[i] == "\n":
                if self.font.size(temp_text + temp_word)[0] >= self.size[0] - 20:
                    self.text.append(temp_text)
                    temp_text = ""
                    temp_word = ""
                else:
                    self.text.append(temp_text + temp_word)
                    temp_text = "" 
                    temp_word = ""
            else:
                temp_word += text[i]
        temp_text += temp_word
        self.text.append(temp_text)
        self.scroll_lock = False
        self.scroll = 0

        # If the length of the text is greater than the size of the box, the user can scroll through it, else the scroll bar is disabled and not drawn
        # The max scroll value is the length of the text minus the size of the box
        if len(self.text) * self.font.size(self.text[0])[1] > self.size[1]:
            self.max_scroll = (len(self.text) + 1) * self.font.size(self.text[0])[1] - self.size[1]
        else:
            self.max_scroll = -1
