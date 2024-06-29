margin_x = 10
margin_y = 4


n_level = 1


def calculate_position_with_margin(x, y) -> tuple:
    return x + margin_x, y + margin_y


def main():
    import pygame
    import load_level
    from sys import exit
    from character import pac_man, ghost

    game_play_status = False
    pygame.init()
    screen = pygame.display.set_mode((960, 540))

    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption("PacMan")

    font = pygame.font.SysFont('Arial', 24)

    # load character
    main_c = pac_man()
    ghost_0 = ghost(0)
    ghost_1 = ghost(1)
    ghost_2 = ghost(2)
    ghost_3 = ghost(3)

    # load point picture
    point_pic = pygame.image.load("./pic/point.png")

    def draw_rec(window, x, y, color_index):
        if color_index == 1:
            pygame.draw.rect(window, (0, 100, 255), pygame.Rect(20 * x, 20 * y, 20, 20))
        elif color_index == 0:
            window.blit(point_pic, (20 * x + margin_x - 10, 20 * y + margin_y - 5))

    # loop that update the screen
    def redraw(window):
        window.fill((0, 0, 0))

        rows = load_level.rows
        columns = load_level.columns

        for row in range(rows):
            for column in range(columns):
                p = calculate_position_with_margin(column, row)
                draw_rec(window, p[0], p[1], load_level.level_array[row * columns + column])

        # draw character
        main_c.draw(window)
        main_c.update_location(load_level.level_array)

        ghost_0.draw(window)
        ghost_1.draw(window)
        ghost_2.draw(window)
        ghost_3.draw(window)

        # draw the point counter
        text_surface = font.render(f'Point left: {load_level.point}', True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (750, 250)
        screen.blit(text_surface, text_rect)

    def print_win_page(window):
        window.fill((0, 0, 0))

        text_surface = font.render('Win!', True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (480, 250)
        screen.blit(text_surface, text_rect)

    while True:
        # get event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        if load_level.level_array is None:
            load_level.load_level(1)

        if load_level.point > 0:
            redraw(screen)
        else:
            print_win_page(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
