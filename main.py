margin_x = 10
margin_y = 4

n_level = 1


def calculate_position_with_margin(x, y) -> tuple:
    return x + margin_x, y + margin_y


def main():
    import pygame
    import load_level
    from sys import exit
    from character import pac_man

    pygame.init()
    screen = pygame.display.set_mode((960, 540))

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

        if load_level.level_array is None:
            load_level.load_level(1)

        rows = load_level.rows
        columns = load_level.columns

        for row in range(rows):
            for column in range(columns):
                p = calculate_position_with_margin(column, row)
                draw_rec(window, p[0], p[1], load_level.level_array[row * columns + column])

        # draw character
        main_c.draw(window)
        main_c.update_location(load_level.level_array)

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
