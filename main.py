import pygame
from load_level import load_to_list
from sys import exit


pygame.init()
screen = pygame.display.set_mode((960, 540))
level_array = rows = columns = None
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption("PacMan")


def draw_rec(window, x, y, color_index):
    if color_index == 1:
        pygame.draw.rect(window, (0, 100, 255), pygame.Rect(20 * x, 20 * y, 20, 20))


def redraw(window):
    window.fill((0, 0, 0))
    margin_x = 4
    margin_y = 10
    global level_array, rows, columns

    if level_array is None:
        data = load_to_list(1)
        level_array = data["data"]
        rows = data["rows"]
        columns = data["columns"]

    for row in range(rows):
        for column in range(columns):
            draw_rec(window, margin_y + column, margin_x + row, level_array[row * columns + column])


# loading picture
man = pygame.image.load('pic/man.png').convert_alpha()
man_x_position = 0

while True:
    # get event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    redraw(screen)
    pygame.display.update()
    clock.tick(FPS)
