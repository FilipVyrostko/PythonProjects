import os

from tic_tac_toe import utils
from tic_tac_toe import minimax


def main() -> int:
    name, rows, columns, position = utils.get_user_settings()

    score: int = 0
    position = position == 1

    player: dict = {"name": name, "is_maximizer": position, "symbol": "X" if position else "O"}
    AI: dict = {"name": "AI", "is_maximizer": not position, "symbol": "X" if not position else "O"}

    os.system("cls")

    # Initializing board
    board: list = []
    for i in range(rows):
        board.append(["-"] * columns)

    moves_left: int = rows * columns

    if not player["is_maximizer"]:
        print("\nAI is making its turn...\n")
        ai_move = minimax.find_best_move(board, AI["is_maximizer"], moves_left)
        board[ai_move[0]][ai_move[1]] = AI["symbol"]

        # Check if new placement causes strikeout
        score += utils.get_score(board, True)
        utils.render(board)
        moves_left -= 1
    else:
        utils.render(board)

    while moves_left:

        row, col = utils.get_user_move(rows, columns, board)

        board[row][col] = player["symbol"]
        moves_left -= 1

        # Check if new placement causes strikeout
        score += utils.get_score(board, True)
        utils.render(board)

        if moves_left:
            print("\nAI is making its turn...\n")
            ai_move = minimax.find_best_move(board, AI["is_maximizer"], moves_left)
            board[ai_move[0]][ai_move[1]] = AI["symbol"]
            moves_left -= 1

            # Check if new placement causes strikeout
            score += utils.get_score(board, True)
            utils.render(board)

    utils.print_score(score, board, player, AI)

    return 0


if __name__ == "__main__":
    main()
