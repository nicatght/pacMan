import pygame
from main import margin_x, margin_y
import load_level as lv

import keyboard
from keyBoard import on_key_press
import random


# return true if collision happen, false otherwise
def exist_collision(x, y, neglect_gate=False) -> bool:
    """
    Check if there is a wall in grid location (x, y)
    :param neglect_gate: decide whether to neglect gate or not (ghost purpose)
    :param x: grid position x
    :param y: grid position y
    :return: True if there is a wall, false otherwise
    """
    if neglect_gate:
        return lv.level_array[y * lv.columns + x] == 1
    return lv.level_array[y * lv.columns + x] == 1 or lv.level_array[y * lv.columns + x] == 5


def update_r_position(direction: str, position, r_position, *, neglect_gate=False) -> tuple:
    """
    This function is used to update element's real position base on its direction and location
    :param direction:
    :param position: the grid position
    :param r_position: the real position print in window
    :param neglect_gate: whether the movement neglect gate or not
    :return: the new r_position
    """
    match direction:
        case "r":
            if not exist_collision(position[0] + 1, position[1], neglect_gate):
                r_position = (r_position[0] + 1, r_position[1])
        case "l":
            if not exist_collision(position[0] - 1, position[1], neglect_gate):
                r_position = (r_position[0] - 1, r_position[1])
        case "u":
            if not exist_collision(position[0], position[1] - 1, neglect_gate):
                r_position = (r_position[0], r_position[1] - 1)
        case "d":
            if not exist_collision(position[0], position[1] + 1, neglect_gate):
                r_position = (r_position[0], r_position[1] + 1)
    if r_position[0] % 20 == 0 and r_position[1] % 20 == 0:
        update_position(position, r_position)
    return r_position


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
        self.direction = "r"

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

    def update_location(self):
        self.r_position = update_r_position(self.direction, self.position, self.r_position)

        # managing changing direction when character is in decision spot
        if self.r_position[0] % 20 == 0 and self.r_position[1] % 20 == 0:
            if lv.level_array[self.position[1] * lv.columns + self.position[0]] == 0:
                lv.level_array[self.position[1] * lv.columns + self.position[0]] = 2
                lv.point -= 1

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


class ghost:
    def __init__(self, id):
        self.is_release = 0  # 0: not release, 1: released, 2 releasing
        match id:
            case 0:
                img = pygame.image.load("./pic/ghost_1.png")
                self.position = [7, 9]
                self.direction = "r"
            case 1:
                img = pygame.image.load("./pic/ghost_2.png")
                self.position = [8, 9]
                self.direction = "r"
            case 2:
                img = pygame.image.load("./pic/ghost_3.png")
                self.position = [10, 9]
                self.direction = "l"
            case 3:
                img = pygame.image.load("./pic/ghost_4.png")
                self.position = [11, 9]
                self.direction = "l"

        self.img = pygame.transform.scale(img, (20, 20))
        self.r_position = [(self.position[0] + margin_x) * 20, (self.position[1] + margin_y) * 20]

    def draw(self, window):
        window.blit(self.img, (self.r_position[0], self.r_position[1]))

    def update_location(self) -> None:
        if self.is_release == 0:  # not release
            return
        elif self.is_release == 1:  # released
            self.r_position = update_r_position(self.direction, self.position, self.r_position)
            if self.r_position[0] % 20 == 0 and self.r_position[1] % 20 == 0:
                self.direction = self.direction_decider(self.direction, self.position)
        else:  # releasing
            self.r_position = update_r_position(self.direction, self.position, self.r_position, neglect_gate=True)
            if self.position == [9, 9]:
                self.direction = "d"
            elif self.position == [9, 11]:
                self.is_release = 1

    @staticmethod
    def direction_decider(direction, position) -> str:
        """

        :param direction: the direction currently the element is heading to
        :param position: the current grid position
        :return: new direction
        """
        directions = {"u", "d", "l", "r"}
        available_dir = set()

        # remove the opposite side
        opposites = {"u": "d", "d": "u", "l": "r", "r": "l"}
        directions.remove(opposites[direction])

        # remove direction that is not available
        for d in directions:
            match d:
                case "u":
                    if not exist_collision(position[0], position[1] - 1):
                        available_dir.add("u")
                case "d":
                    if not exist_collision(position[0], position[1] + 1):
                        available_dir.add("d")
                case "l":
                    if not exist_collision(position[0] - 1, position[1]):
                        available_dir.add("l")
                case "r":
                    if not exist_collision(position[0] + 1, position[1]):
                        available_dir.add("r")

        return random.choice(list(available_dir))

    def release(self) -> None:
        self.is_release = 2
