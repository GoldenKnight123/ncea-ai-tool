import pygame

#Basic button class
#size: tuple (width, height)
#pos: tuple (x, y)
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
        