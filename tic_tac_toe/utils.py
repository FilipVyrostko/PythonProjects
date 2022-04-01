import os
import sys
import time

import numpy as np


def get_user_settings() -> tuple:
    print("\nWELCOME TO GAME OF TIC TAC TOE\n")
    name = input("Please, enter your name: ")
    rows = input("Please enter the number of rows of the board: ")
    columns = input("Please enter the number of columns of the board: ")
    position = input("If you want to go first, enter 1, if you wish to go second, enter 2: ")

    if not validate(rows, columns, position, cast=int):
        print("\nOnly numbers can be entered\n")
        sys.exit(1)

    rows, columns, position = int(rows), int(columns), int(position)

    if rows < 3 or columns < 3:
        print("\nSmallest permitted board is 3x3\n")
        print("Setting board to 3x3\n")
        rows, columns = 3, 3
    if position not in (1, 2):
        print("\nWrong position value entered\n")
        print("Setting position to 1\n")
        position = 1

    return name, rows, columns, position


def get_user_move(rows, columns, board) -> tuple:
    row = input("Please enter the number of the row you wish to place your symbol in: ")
    col = input("Please enter the number of the column you wish to place your symbol in: ")

    if not validate(row, col, cast=int):
        print("\nOnly numbers can be entered\n")
        sys.exit(0)

    row, col = int(row) - 1, int(col) - 1

    while row < 0 or row >= rows or col < 0 or col >= columns:
        print("\nInvalid row or column number entered... try again\n")
        row = input("Please enter the number of the row you wish to place your symbol in: ")
        col = input("Please enter the number of the column you wish to place your symbol in: ")

        if not validate(row, col, cast=int):
            print("\nOnly numbers can be entered\n")
            sys.exit(0)

        row, col = int(row) - 1, int(col) - 1

    while board[row][col] != "-":
        print("\nPosition already occupied, choose different place...\n")
        row = input("Please enter the number of the row you wish to place your symbol in: ")
        col = input("Please enter the number of the column you wish to place your symbol in: ")

        if not validate(row, col, cast=int):
            print("\nOnly numbers can be entered\n")
            sys.exit(0)

        row, col = int(row) - 1, int(col) - 1

    return row, col


def validate(*args, cast) -> bool:
    try:
        for arg in args:
            cast(arg)
        return True
    except ValueError:
        return False


def get_score(board: list, strikeout: bool) -> int:
    score = 0

    strikeout_x: str = 'X' + '\u0336'
    strikeout_o: str = 'O' + '\u0336'

    b_col: int = len(board[0])  # Number of columns
    b_row: int = len(board)  # Number of rows

    # Check rows
    for row in range(0, b_row):
        for col in range(1, b_col - 1):
            if board[row][col - 1] == "X" and board[row][col] == "X" and board[row][col + 1] == "X":
                if strikeout:
                    # Add strikeout for X
                    board[row][col - 1], board[row][col], board[row][col + 1] = strikeout_x, strikeout_x, strikeout_x

                score += 10
            elif board[row][col - 1] == "O" and board[row][col] == "O" and board[row][col + 1] == "O":

                if strikeout:
                    # Add strikeout for O
                    board[row][col - 1], board[row][col], board[row][col + 1] = strikeout_o, strikeout_o, strikeout_o

                score -= 10

    # Check columns
    for col in range(0, b_col):
        for row in range(1, b_row - 1):
            if board[row - 1][col] == "X" and board[row][col] == "X" and board[row + 1][col] == "X":

                if strikeout:
                    # Add strikeout for X
                    board[row - 1][col], board[row][col], board[row + 1][col] = strikeout_x, strikeout_x, strikeout_x

                score += 10
            elif board[row - 1][col] == "O" and board[row][col] == "O" and board[row + 1][col] == "O":

                if strikeout:
                    # Add strikeout for O
                    board[row - 1][col], board[row][col], board[row + 1][col] = strikeout_o, strikeout_o, strikeout_o

                score -= 10

    # Check diagonal (both ways)
    for row in range(1, b_row - 1):
        for col in range(1, b_col - 1):

            # Check diagonal left to right
            if board[row - 1][col - 1] == "X" and board[row][col] == "X" and board[row + 1][col + 1] == "X":

                if strikeout:
                    # Add strikeout for X
                    board[row - 1][col - 1], board[row][col], board[row + 1][col + 1] = \
                        strikeout_x, strikeout_x, strikeout_x

                score += 10
            elif board[row - 1][col - 1] == "O" and board[row][col] == "O" and board[row + 1][col + 1] == "O":

                if strikeout:
                    # Add strikeout for O
                    board[row - 1][col - 1], board[row][col], board[row + 1][col + 1] = \
                        strikeout_o, strikeout_o, strikeout_o

                score -= 10

            # Check diagonal right to left
            if board[row - 1][col + 1] == "X" and board[row][col] == "X" and board[row + 1][col - 1] == "X":

                if strikeout:
                    # Add strikeout for X
                    board[row - 1][col + 1], board[row][col], board[row + 1][col - 1] = \
                        strikeout_x, strikeout_x, strikeout_x

                score += 10
            elif board[row - 1][col + 1] == "O" and board[row][col] == "O" and board[row + 1][col - 1] == "O":

                if strikeout:
                    # Add strikeout for O
                    board[row - 1][col + 1], board[row][col], board[row + 1][col - 1] = \
                        strikeout_o, strikeout_o, strikeout_o

                score -= 10

    return score


def print_score(score, board, player, AI) -> None:
    os.system("cls")

    if player.is_maximizer and score > 0 or not player.is_maximizer and score < 0:
        print(f"Congratulations! You have won! Score: {abs(score)}")
    elif AI.is_maximizer and score > 0 or not AI.is_maximizer and score < 0:
        print(f"AI has won. Final score: {abs(score)}")
    else:
        print("It's a Draw.")

    render(board)


def render(board) -> None:
    time.sleep(2)
    os.system("cls")
    matrix = np.array(board)
    print(matrix)
