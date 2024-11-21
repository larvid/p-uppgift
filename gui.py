import pygame as pg
import p_uppgift

pg.init()

WIDTH, HEIGHT = 500, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Knight Walk Simulator")
# colors
OFF_WHITE = (238, 238, 210)
OFF_WHITE_HIGHLIGHT = (201, 201, 188)
GREEN = (118, 150, 86)
GREEN_HIGHLIGHT = (70, 100, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG = (161, 102, 47)
font = pg.font.Font(None, 36)
small_font = pg.font.Font(None, 22)

# global list with information regarding squares, such as position and coordinates
squares = []
square_pos = []
clicked_states = []
square_color = []

# generate squares in board
for board_row in range(8):
    for board_col in range(8):
        squares.append(pg.Rect(board_col * 50 + 50, board_row * 50 + 25, 50, 50))
        square_pos.append((board_row, board_col))
        clicked_states.append(False)
        if (board_row + board_col) % 2 == 0:
            square_color.append(OFF_WHITE)
        else:
            square_color.append(GREEN)

# generate outline
outline = pg.Rect(40, 15, 420, 420)

# main menu buttons
menu = []
for menu_buttons in range(4):
    button = pg.Rect(menu_buttons * 120 + 20, 500, 100, 50)
    menu.append(button)


def render_board():
    # render squares in board
    for i, square in enumerate(squares):
        pg.draw.rect(screen, square_color[i], square)
    pg.draw.rect(screen, BG, (0, 460, 500, 40))


def initial_render():
    # background color
    screen.fill(BG)
    # board outline
    pg.draw.rect(screen, BLACK, outline)
    # numbers
    for number in range(8):
        screen.blit(font.render(str(8 - number), True, BLACK), (23, number * 50 + 40))
    # letters
    for letter in range(8):
        screen.blit(
            font.render((chr(int(letter) + 97)).upper(), True, BLACK),
            (letter * 50 + 65, 436),
        )
    # main menu
    for i, button in enumerate(menu):
        pg.draw.rect(screen, OFF_WHITE, button)

    text_0 = small_font.render("Walk", True, BLACK)
    text_1 = small_font.render("Random", True, BLACK)
    text_2 = small_font.render("Complete", True, BLACK)
    text_3 = small_font.render("Manual", True, BLACK)
    text_4 = small_font.render("Quit", True, BLACK)
    screen.blit(text_1, (menu[0].x + 18, menu[0].y + 8))
    screen.blit(text_0, (menu[0].x + 31, menu[0].y + 28))
    screen.blit(text_2, (menu[1].x + 15, menu[1].y + 8))
    screen.blit(text_0, (menu[1].x + 31, menu[1].y + 28))
    screen.blit(text_3, (menu[2].x + 20, menu[2].y + 8))
    screen.blit(text_0, (menu[2].x + 31, menu[2].y + 28))
    screen.blit(text_4, (menu[3].x + 31, menu[3].y + 17))


def knight_pos(knight_row, knight_col):
    # movement of the knight
    # knight PNG from https://pngtree.com/freepng/chess-knight-horse-logo-illustration_4275224.html
    knight_image = pg.image.load("knight.png")
    scaled_knight = pg.transform.scale(knight_image, (50, 50))
    screen.blit(scaled_knight, (50 + knight_col * 50, 25 + knight_row * 50))


def rand_walk(board, knight_row, knight_col):
    p_uppgift.rand_walk(board, knight_row, knight_col)
    move_nr = 2
    move_check = 1
    while move_check != move_nr:
        for i in range(8):
            for j in range(8):
                if board[i][j] == move_nr:
                    prev_row, prev_col = knight_row, knight_col
                    knight_row, knight_col = i, j
                    knight_pos(knight_row, knight_col)
                    for n, pos in enumerate(square_pos):
                        if (prev_row, prev_col) == pos:
                            if square_color[n] == GREEN:
                                prev_square_color = GREEN_HIGHLIGHT
                            else:
                                prev_square_color = OFF_WHITE_HIGHLIGHT
                            pg.draw.rect(screen, prev_square_color, squares[n])
                            nr = font.render(str(move_nr - 1), True, BLACK)
                            horizontal = 68
                            if move_nr > 10:  # centers numbers over 9
                                horizontal -= 7
                            screen.blit(
                                nr, (horizontal + prev_col * 50, 40 + prev_row * 50)
                            )
                    move_nr += 1
                    pg.time.delay(100)
                    pg.display.update()
        move_check += 1
    return True


def complete_walk(board, knight_row, knight_col):
    p_uppgift.complete_walk(board, knight_row, knight_col, depth=1)
    move_nr = 1
    for square in range(63):
        for i in range(8):
            for j in range(8):
                if board[i][j] == square + 2:
                    prev_row, prev_col = knight_row, knight_col
                    knight_row, knight_col = i, j
                    knight_pos(knight_row, knight_col)
                    for n, pos in enumerate(square_pos):
                        if (prev_row, prev_col) == pos:
                            if square_color[n] == GREEN:
                                prev_square_color = GREEN_HIGHLIGHT
                            else:
                                prev_square_color = OFF_WHITE_HIGHLIGHT
                            pg.draw.rect(screen, prev_square_color, squares[n])
                            nr = font.render(str(move_nr), True, BLACK)
                            horizontal = 68
                            if move_nr > 9:  # centers numbers over 9
                                horizontal -= 7
                            screen.blit(
                                nr, (horizontal + prev_col * 50, 40 + prev_row * 50)
                            )
                    move_nr += 1
                    pg.time.delay(100)
                    pg.display.update()
    return True


# lägg till meddeladen för om man får över 60 och riktigt fett om man får 64
def man_walk(menu, board, knight_row, knight_col, square_pos):
    move_nr = 1
    while True:
        clickable_squares = []
        clickable_squares_pos = []
        moves = p_uppgift.candidate_moves(board, knight_row, knight_col)
        for i in range(len(square_pos)):
            for j in range(len(moves)):
                if square_pos[i] == moves[j]:
                    move_row, move_col = square_pos[i]
                    if square_color[i] == GREEN:
                        move_color = GREEN
                        circle_color = GREEN_HIGHLIGHT
                    else:
                        move_color = OFF_WHITE
                        circle_color = OFF_WHITE_HIGHLIGHT
                    pg.draw.circle(
                        screen,
                        circle_color,
                        (75 + move_col * 50, 50 + move_row * 50),
                        10,
                        0,
                    )
                    clickable_squares.append(squares[i])
                    clickable_squares_pos.append(square_pos[i])
        pg.display.update()
        if len(moves) == 0:
            return True
        click = False
        while not click:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    for i, square in enumerate(clickable_squares):
                        if square.collidepoint(mouse_pos):
                            clicked_states = [False] * 64
                            prev_row, prev_col = knight_row, knight_col
                            knight_row, knight_col = clickable_squares_pos[i]
                            board[knight_row][knight_col] = move_nr
                            clicked_states[i] = not clicked_states[i]
                            click = True
                    if menu[3].collidepoint(mouse_pos):
                        return True
        for square in clickable_squares:
            pg.draw.rect(screen, move_color, square)
        if circle_color == GREEN_HIGHLIGHT:
            prev_pos_color = OFF_WHITE_HIGHLIGHT
        else:
            prev_pos_color = GREEN_HIGHLIGHT
        pg.draw.rect(
            screen, prev_pos_color, (prev_col * 50 + 50, prev_row * 50 + 25, 50, 50)
        )
        nr = font.render(str(move_nr), True, BLACK)
        horizontal = 68
        if move_nr > 9:  # centers numbers over 9
            horizontal -= 7
        screen.blit(nr, (horizontal + prev_col * 50, 40 + prev_row * 50, 50, 50))
        knight_pos(knight_row, knight_col)
        move_nr += 1


def freeze_until_quit(menu):
    press_to_contine = font.render("Press 'Quit' to continue", True, BLACK)
    screen.blit(press_to_contine, (113, 460))
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if menu[3].collidepoint(mouse_pos):
                    return True


def starting_position(squares, menu):
    choose_move = font.render("Choose your starting move", True, BLACK)
    screen.blit(choose_move, (90, 462))
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i, square in enumerate(squares):
                    if square.collidepoint(mouse_pos):
                        clicked_states = [False] * 64
                        knight_row, knight_col = square_pos[i]
                        clicked_states[i] = not clicked_states[i]
                        return knight_row, knight_col
                if menu[3].collidepoint(mouse_pos):
                    pg.quit()
                    exit()


def main():
    initial_render()
    render_board()
    knight_row, knight_col = starting_position(squares, menu)
    board = p_uppgift.generate_board(knight_row, knight_col)
    render_board()
    knight_pos(knight_row, knight_col)
    change_move_text = font.render("Click on the board to change move", True, BLACK)
    screen.blit(change_move_text, (50, 462))
    pg.display.update()

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # mouse1 click detection
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if outline.collidepoint(mouse_pos):
                    render_board()
                    knight_row, knight_col = starting_position(squares, menu)
                if menu[0].collidepoint(mouse_pos):
                    render_board()
                    rand_walk(board, knight_row, knight_col)
                    freeze_until_quit(menu)
                if menu[1].collidepoint(mouse_pos):
                    render_board()
                    complete_walk(board, knight_row, knight_col)
                    freeze_until_quit(menu)
                if menu[2].collidepoint(mouse_pos):
                    render_board()
                    knight_pos(knight_row, knight_col)
                    man_walk(menu, board, knight_row, knight_col, square_pos)
                    freeze_until_quit(menu)
                if menu[3].collidepoint(mouse_pos):
                    running = False

                render_board()
                board = p_uppgift.generate_board(knight_row, knight_col)
                knight_pos(knight_row, knight_col)
                screen.blit(change_move_text, (50, 462))
                pg.display.flip()
    pg.quit()


if __name__ == "__main__":
    main()
