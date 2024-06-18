import pygame
from main import margin_x, margin_y


class pac_man:
    def __init__(self):
        # load the picture
        self.character = pygame.image.load("./pic/man.png")
        self.character = pygame.transform.scale(self.character, (20, 20))
        self.direction = "r"

        self.position = [15, 9]

    def draw(self, window):
        position = ((self.position[1] + margin_x) * 20, (self.position[0] + margin_y) * 20)
        window.blit(self.character, position)

