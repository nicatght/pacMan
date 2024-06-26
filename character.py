import pygame
from main import margin_x, margin_y
import load_level as lv

import keyboard
from keyBoard import on_key_press


# return true if collision happen, false otherwise
def exist_collision(x, y) -> bool:
    """
    Check if there is a wall in grid location (x, y)
    :param x: grid position x
    :param y: grid position y
    :return: True if there is a wall, false otherwise
    """
    return lv.level_array[y * lv.columns + x] == 1


def update_position(position, r_position) -> None:
    """
    This function is used to update grid position
    Noticing that the unit is fixed in this scenario (20)

    :param position: the grid position, which is used to align with data
    :param r_position: the actual position where the character is drawn
    :return: None
    """
    position[0] = (r_position[0] // 20) - margin_x
    position[1] = (r_position[1] // 20) - margin_y


class pac_man:
    def __init__(self):
        # load the picture
        self.character = pygame.image.load("./pic/man.png")
        self.character = pygame.transform.scale(self.character, (20, 20))
        self.cache_direction = ''
        self.direction = "l"

        self.position = [9, 15]
        self.r_position = [(self.position[0] + margin_x) * 20, (self.position[1] + margin_y) * 20]
        keyboard.on_press(lambda event: on_key_press(event, self))

    def draw(self, window):
        # do rotation
        match self.direction:
            case "r":
                img = pygame.transform.rotate(self.character, 0)
            case "l":
                img = pygame.transform.rotate(self.character, 180)
            case "u":
                img = pygame.transform.rotate(self.character, 90)
            case "d":
                img = pygame.transform.rotate(self.character, 270)

        window.blit(img, (self.r_position[0], self.r_position[1]))

    def update_location(self, level_array: list):

        match self.direction:
            case "r":
                if not exist_collision(self.position[0] + 1, self.position[1]):
                    self.r_position = (self.r_position[0] + 1, self.r_position[1])
            case "l":
                if not exist_collision(self.position[0] - 1, self.position[1]):
                    self.r_position = (self.r_position[0] - 1, self.r_position[1])
            case "u":
                if not exist_collision(self.position[0], self.position[1] - 1):
                    self.r_position = (self.r_position[0], self.r_position[1] - 1)
            case "d":
                if not exist_collision(self.position[0], self.position[1] + 1):
                    self.r_position = (self.r_position[0], self.r_position[1] + 1)

        if self.r_position[0] % 20 == 0 and self.r_position[1] % 20 == 0:
            update_position(self.position, self.r_position)
            if self.cache_direction != "":
                match self.cache_direction:
                    case "r":
                        if not exist_collision(self.position[0] + 1, self.position[1]):
                            self.direction = "r"
                            self.cache_direction = ""
                    case "l":
                        if not exist_collision(self.position[0] - 1, self.position[1]):
                            self.direction = "l"
                            self.cache_direction = ""
                    case "u":
                        if not exist_collision(self.position[0], self.position[1] - 1):
                            self.direction = "u"
                            self.cache_direction = ""
                    case "d":
                        if not exist_collision(self.position[0], self.position[1] + 1):
                            self.direction = "d"
                            self.cache_direction = ""
