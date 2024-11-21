import random
from typed_input import *


def generate_board(row, col):
    board = [[0 for i in range(8)] for j in range(8)]
    board[row][col] = 1
    return board


def starting_move():
    scol, srow = chess_input("Starting move:")
    row = 8 - int(srow)
    col = int(ord(scol) - 97)
    return (row, col)


def candidate_moves(board, row, col):
    possible_moves = []
    moves = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
    for move in moves:
        nrow = row + move[0]
        ncol = col + move[1]
        if 0 <= nrow < 8 and 0 <= ncol < 8:
            if board[nrow][ncol] == 0:
                possible_moves.append((nrow, ncol))
    return possible_moves


def rand_walk(board, row, col):
    moves = candidate_moves(board, row, col)
    move_nr = 2
    while len(moves) > 0:
        row, col = random.choice(moves)
        board[row][col] = move_nr
        moves = candidate_moves(board, row, col)
        move_nr += 1


def possible_moves(board, row, col):
    count = 0
    moves = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
    for move in moves:
        nrow = row + move[0]
        ncol = col + move[1]
        if 0 <= nrow < 8 and 0 <= ncol < 8:
            if board[nrow][ncol] == 0:
                count += 1
    return count


def warnsdorff_moves(board, row, col):
    moves = candidate_moves(board, row, col)
    moves_sorted = sorted(
        moves, key=lambda move: possible_moves(board, move[0], move[1])
    )
    return moves_sorted


def complete_walk(board, row, col, depth=1):
    if depth == 64:
        return True
    for nrow, ncol in warnsdorff_moves(board, row, col):
        board[nrow][ncol] = depth + 1
        if complete_walk(board, nrow, ncol, depth + 1):
            return True
        board[nrow][ncol] = 0
    return False


def manual_alternatives(board, moves, row, col):
    print_board(board)
    print("-----------------------------------------------------------------------")
    print(f"The moves you can choose from are:")
    choice_nr = 1
    for move in moves:
        row, col = move
        srow = str(8 - row)
        scol = (chr(int(col) + 97)).upper()
        print(f"({choice_nr}) {scol}{srow} ", end="")
        choice_nr += 1
    return "\nQuit (Q)\n"


def manual_walk(board, row, col):
    move_nr = 2
    moves = candidate_moves(board, row, col)
    while (
        choice := input(manual_alternatives(board, moves, row, col)).lower().strip()
    ) != "q":
        if choice == "":
            break
        if 1 <= int(choice) <= len(moves):
            row, col = moves[int(choice) - 1]
            board[row][col] = move_nr
            moves = candidate_moves(board, row, col)
            move_nr += 1
        if len(moves) == 0:
            print("You are out of moves!\n")
            break
    pass


INTRO = """\
Knight Walk Simulator"""

MENU = """\
-----------------------------------------------------------------------
Random Walk (r) Complete Walk (c) Manual Walk (m) New Starting Move (n)
Quit (Q)\n"""


def print_board(board):
    for row in board:
        print(row)


def main_menu():
    return input(MENU)


def main():
    print(INTRO)
    row, col = starting_move()
    board = generate_board(row, col)
    print_board(board)
    while (menu := main_menu().lower().strip()) != "q":
        board = generate_board(row, col)
        if menu == "r":
            rand_walk(board, row, col)
        elif menu == "c":
            complete_walk(board, row, col)
        elif menu == "m":
            manual_walk(board, row, col)
        elif menu == "n":
            row, col = starting_move()
            board = generate_board(row, col)
        elif menu == "":
            break
        print_board(board)


if __name__ == "__main__":
    main()
