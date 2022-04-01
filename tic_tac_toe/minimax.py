from tic_tac_toe import utils

MAX_DEPTH = 5


def find_best_move(board, is_maximizer, moves_left) -> list:
    best_row: int = 0
    best_col: int = 0

    if is_maximizer:
        best_val: int = -(2 ^ 32)

        for row in range(0, len(board)):
            for col in range(0, len(board[0])):
                if board[row][col] == "-":

                    board[row][col] = "X"

                    moves_left -= 1

                    move_val = max(best_val,
                                   minimax(board, depth=MAX_DEPTH, alpha=(2 ^ 32), beta=-(2 ^ 32),
                                           is_maximizer=not is_maximizer, moves_left=moves_left))

                    moves_left += 1
                    board[row][col] = "-"

                    if move_val > best_val:
                        best_row = row
                        best_col = col
                        best_val = move_val

    else:
        best_val: int = (2 ^ 32)

        for row in range(0, len(board)):
            for col in range(0, len(board[0])):
                if board[row][col] == "-":

                    board[row][col] = "O"

                    moves_left -= 1

                    move_val = min(best_val,
                                   minimax(board, depth=MAX_DEPTH, alpha=-(2 ^ 32), beta=(2 ^ 32),
                                           is_maximizer=not is_maximizer, moves_left=moves_left))

                    moves_left += 1
                    board[row][col] = "-"

                    if move_val < best_val:
                        row = row
                        best_col = col
                        best_val = move_val

    return [best_row, best_col]


def minimax(board, depth, alpha, beta, is_maximizer, moves_left) -> int:
    if not moves_left or depth == 0:
        return utils.get_score(board)

    if is_maximizer:
        best_val: int = -(2 ^ 32)

        for row in range(0, len(board)):
            for col in range(0, len(board[0])):
                if board[row][col] == "-":
                    board[row][col] = "X"

                    moves_left -= 1

                    best_val = max(best_val,
                                   minimax(board, depth - 1, alpha, beta, not is_maximizer, moves_left)
                                   )

                    moves_left += 1
                    board[row][col] = "-"

                    alpha = max(alpha, best_val)
                    if beta <= alpha:
                        return best_val

        return best_val

    else:
        best_val: int = (2 ^ 32)

        for row in range(0, len(board)):
            for col in range(0, len(board[0])):
                if board[row][col] == "-":
                    board[row][col] = "O"
                    moves_left -= 1

                    best_val = min(best_val, minimax(board, depth - 1, alpha, beta, not is_maximizer, moves_left))

                    moves_left += 1
                    board[row][col] = "-"

                    beta = min(beta, best_val)
                    if beta <= alpha:
                        return best_val

        return best_val
