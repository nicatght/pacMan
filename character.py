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
    if r_position[0] % 20 == 0 or r_position[1] % 20 == 0:
        position[0] = (r_position[0] // 20) - margin_x
        position[1] = (r_position[1] // 20) - margin_y


class pac_man:
    def __init__(self):
        # load the picture
        self.character = pygame.image.load("./pic/man.png")
        self.character = pygame.transform.scale(self.character, (20, 20))
        self.cache_direction = ''
        self.direction = "r"

        self.position = [15, 9]
        self.r_position = [(self.position[1] + margin_x) * 20, (self.position[0] + margin_y) * 20]
        keyboard.on_press(lambda event: on_key_press(event, self))

    def draw(self, window):
        window.blit(self.character, (self.r_position[0], self.r_position[1]))

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

        update_position(self.position, self.r_position)
