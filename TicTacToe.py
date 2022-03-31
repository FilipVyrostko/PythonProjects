import os
import time

import numpy as np

max_depth = 5

class Player:

    def __init__(self, name, is_maximizer):
        self.name = name
        self.is_maximizer = is_maximizer

        if is_maximizer:
            self.symbol = "X"
        else:
            self.symbol = "O"

    def __str__(self):
        return "Player Name: {name} -- Player Symbol: {symbol}".format(name=self.name, symbol=self.symbol)


def main():
    print("\nWELCOME TO GAME OF TIC TAC TOE\n")
    name = input("Please, enter your name: ")
    rows = input("Please enter the number of rows of the board: ")
    columns = input("Please enter the number of columns of the board: ")
    position = input("If you want to go first, enter 1, if you wish to go second, enter 2: ")

    if not validate(rows, columns, position, cast=int):
        print("\nOnly numbers can be entered\n")
        exit(1)

    rows, columns, position = int(rows), int(columns), int(position)

    if rows < 3 or columns < 3:
        print("\nSmallest permitted board is 3x3\n")
        print("Setting board to 3x3\n")
        rows, columns = 3, 3
    if position != 1 and position != 2:
        print("\nWrong position value entered\n")
        print("Setting position to 1\n")

    position = position == 1

    player = Player(name, is_maximizer=position)
    AI = Player("AI", is_maximizer=not position)

    os.system("cls")
    print("Game info: {player1} || {AI}".format(player1=player.__str__(), AI=AI.__str__()))

    # Initializing board
    board = []
    for i in range(rows):
        board.append(["-"] * columns)

    moves_left = rows * columns

    if not player.is_maximizer:
        print("\nAI is making its turn...\n")
        ai_move = find_best_move(board, player.is_maximizer)
        board[ai_move[0]][ai_move[1]] = AI.symbol
        render(board)
        moves_left -= 1
    else:
        render(board)

    while moves_left:
        row = input("Please enter the number of the row you wish to place your symbol in: ")
        col = input("Please enter the number of the column you wish to place your symbol in: ")

        if not validate(row, col, cast=int):
            print("\nOnly numbers can be entered\n")
            exit(0)

        row, col = int(row) - 1, int(col) - 1

        while row < 0 or row >= rows or col < 0 or col >= columns:
            print("\nInvalid row or column number entered... try again\n")
            row = input("Please enter the number of the row you wish to place your symbol in: ")
            col = input("Please enter the number of the column you wish to place your symbol in: ")

            if not validate(row, col, cast=int):
                print("\nOnly numbers can be entered\n")
                exit(0)

            row, col = int(row) - 1, int(col) - 1

        while board[row][col] != "-":
            print("\nPosition already occupied, choose different place...\n")
            row = input("Please enter the number of the row you wish to place your symbol in: ")
            col = input("Please enter the number of the column you wish to place your symbol in: ")

            if not validate(row, col, cast=int):
                print("\nOnly numbers can be entered\n")
                exit(0)

            row, col = int(row) - 1, int(col) - 1

        board[row][col] = player.symbol
        moves_left -= 1
        render(board)

        if moves_left:
            print("\nAI is making its turn...\n")
            ai_move = find_best_move(board, AI.is_maximizer, moves_left)
            board[ai_move[0]][ai_move[1]] = AI.symbol
            moves_left -= 1
            render(board)

    score = get_score(board)
    if player.is_maximizer and score > 0 or not player.is_maximizer and score < 0:
        print(f"Congratulations! You have won! Score: {abs(score)}")
    elif AI.is_maximizer and score > 0 or not AI.is_maximizer and score < 0:
        print(f"AI has won. Final score: {abs(score)}")
    else:
        print("It's a Draw.")

    return 0


def validate(*args, cast):
    try:
        for arg in args:
            cast(arg)
        return True
    except:
        return False


def find_best_move(board, is_maximizer, moves_left):
    row = 0
    col = 0

    if is_maximizer:
        best_val = -(2 ^ 32)

        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                if board[r][c] == "-":

                    board[r][c] = "X"

                    moves_left -= 1

                    move_val = max(best_val, minimax(board, depth=max_depth, alpha=(2 ^ 32), beta=-(2 ^ 32),
                                                     is_maximizer=not is_maximizer, moves_left=moves_left))
                    moves_left += 1
                    board[r][c] = "-"

                    if move_val > best_val:
                        row = r
                        col = c
                        best_val = move_val

    else:
        best_val = (2 ^ 32)

        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                if board[r][c] == "-":

                    board[r][c] = "O"

                    moves_left -= 1

                    move_val = min(best_val, minimax(board, depth=max_depth, alpha=-(2 ^ 32), beta=(2 ^ 32),
                                                     is_maximizer=not is_maximizer, moves_left=moves_left))
                    moves_left += 1
                    board[r][c] = "-"

                    if move_val < best_val:
                        row = r
                        col = c
                        best_val = move_val

    return [row, col]


def minimax(board, depth, alpha, beta, is_maximizer, moves_left):

    if not moves_left or depth == 0:
        return get_score(board)

    if is_maximizer:
        best_val = -(2 ^ 32)

        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                if board[r][c] == "-":
                    board[r][c] = "X"

                    moves_left -= 1

                    best_val = max(best_val, minimax(board, depth - 1, alpha, beta, not is_maximizer, moves_left))

                    moves_left += 1
                    board[r][c] = "-"

                    alpha = max(alpha, best_val)
                    if beta <= alpha:
                        return get_score(board)

    else:
        best_val = (2 ^ 32)

        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                if board[r][c] == "-":
                    board[r][c] = "O"
                    moves_left -= 1

                    best_val = min(best_val, minimax(board, depth - 1, alpha, beta, not is_maximizer, moves_left))

                    moves_left += 1
                    board[r][c] = "-"

                    beta = min(beta, best_val)
                    if beta <= alpha:
                        return get_score(board)

    return best_val


def get_score(board):
    score = 0

    col = len(board[0])  # Number of columns
    row = len(board)  # Number of rows

    # Check rows
    for r in range(0, row):
        for c in range(1, col - 1):
            if board[r][c - 1] == "X" and board[r][c] == "X" and board[r][c + 1] == "X":
                score += 10
            elif board[r][c - 1] == "O" and board[r][c] == "O" and board[r][c + 1] == "O":
                score -= 10

    # Check columns
    for r in range(1, row - 1):
        for c in range(0, col):
            if board[r - 1][c] == "X" and board[r][c] == "X" and board[r + 1][c] == "X":
                score += 10
            elif board[r - 1][c] == "O" and board[r][c] == "O" and board[r + 1][c] == "O":
                score -= 10

    # Check diagonal (both ways)
    for r in range(1, row - 1):
        for c in range(1, col - 1):

            if board[r - 1][c - 1] == "X" and board[r][c] == "X" and board[r + 1][c + 1] == "X" \
                    or board[r - 1][c + 1] == "X" and board[r][c] == "X" and board[r + 1][c - 1] == "X":
                score += 10

            elif board[r - 1][c - 1] == "O" and board[r][c] == "O" and board[r + 1][c + 1] == "O" \
                    or board[r - 1][c + 1] == "O" and board[r][c] == "O" and board[r + 1][c - 1] == "O":
                score -= 10

    return score


def render(board):
    col = len(board[0])  # Number of columns
    row = len(board)  # Number of rows

    time.sleep(2)
    os.system("cls")
    matrix = np.array(board)
    print(matrix)


if __name__ == "__main__":
    main()
