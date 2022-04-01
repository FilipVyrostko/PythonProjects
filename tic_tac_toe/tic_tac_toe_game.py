import os

from tic_tac_toe import utils
from tic_tac_toe import minimax


class Player:

    def __init__(self, name, is_maximizer):
        self.name = name
        self.is_maximizer = is_maximizer

        if is_maximizer:
            self.symbol = "X"
        else:
            self.symbol = "O"

    def __str__(self):
        return f"Player Name: {self.name} -- Player Symbol: {self.symbol}"


def main():
    name, rows, columns, position = utils.get_user_settings()

    position = position == 1

    player = Player(name, is_maximizer=position)
    AI = Player("AI", is_maximizer=not position)

    os.system("cls")
    print(f"Game info: {player.__str__()} || {AI.__str__()}")

    # Initializing board
    board = []
    for i in range(rows):
        board.append(["-"] * columns)

    moves_left = rows * columns

    if not player.is_maximizer:
        print("\nAI is making its turn...\n")
        ai_move = minimax.find_best_move(board, player.is_maximizer, moves_left)
        board[ai_move[0]][ai_move[1]] = AI.symbol
        utils.render(board)
        moves_left -= 1
    else:
        utils.render(board)

    while moves_left:

        row, col = utils.get_user_move(rows, columns, board)

        board[row][col] = player.symbol
        moves_left -= 1
        utils.render(board)

        if moves_left:
            print("\nAI is making its turn...\n")
            ai_move = minimax.find_best_move(board, AI.is_maximizer, moves_left)
            board[ai_move[0]][ai_move[1]] = AI.symbol
            moves_left -= 1
            utils.render(board)

    utils.print_score(board, player, AI)

    return 0


if __name__ == "__main__":
    main()
