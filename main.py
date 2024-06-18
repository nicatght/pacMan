margin_x = 10
margin_y = 4


def calculate_position_with_margin(x, y) -> tuple:
    return x + margin_x, y + margin_y


def main():
    import pygame
    from load_level import load_to_list
    from sys import exit
    from character import pac_man

    pygame.init()
    screen = pygame.display.set_mode((960, 540))
    level_array = rows = columns = None
    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption("PacMan")

    # load character
    main_c = pac_man()

    def draw_rec(window, x, y, color_index):
        if color_index == 1:
            pygame.draw.rect(window, (0, 100, 255), pygame.Rect(20 * x, 20 * y, 20, 20))

    def redraw(window):
        window.fill((0, 0, 0))

        nonlocal level_array, rows, columns

        if level_array is None:
            data = load_to_list(1)
            level_array = data["data"]
            rows = data["rows"]
            columns = data["columns"]

        for row in range(rows):
            for column in range(columns):
                p = calculate_position_with_margin(column, row)
                draw_rec(window, p[0], p[1], level_array[row * columns + column])

        # draw character
        main_c.draw(window)

    while True:
        # get event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        redraw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
