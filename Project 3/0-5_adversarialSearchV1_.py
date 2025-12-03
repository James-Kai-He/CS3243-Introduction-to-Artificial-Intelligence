class Piece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type
        self.color = color
        self.position = position

    def get_moves(self, board):
        moves = []
        if self.piece_type == "King":
            moves = self.get_king_moves(board)
        elif self.piece_type == "Rook":
            moves = self.get_rook_moves(board)
        elif self.piece_type == "Bishop":
            moves = self.get_bishop_moves(board)
        elif self.piece_type == "Knight":
            moves = self.get_knight_moves(board)
        elif self.piece_type == "Squire":
            moves = self.get_squire_moves(board)
        elif self.piece_type == "Combatant":
            moves = self.get_combatant_moves(board)
        return moves

    def get_king_moves(self, board):
        moves = []
        row, col = self.position
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        for d_row, d_col in directions:
            new_pos = (row + d_row, col + d_col)
            if board.is_within_bounds(new_pos) and (
                not board.get_piece_at(new_pos)
                or board.get_piece_at(new_pos).color != self.color
            ):
                moves.append((self.position, new_pos))
        return moves

    def get_rook_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d_row, d_col in directions:
            for i in range(1, 8):
                new_pos = (row + i * d_row, col + i * d_col)
                if not board.is_within_bounds(new_pos):
                    break
                target_piece = board.get_piece_at(new_pos)
                if target_piece:
                    if target_piece.color != self.color:
                        moves.append((self.position, new_pos))
                    break
                moves.append((self.position, new_pos))
        return moves

    def get_bishop_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d_row, d_col in directions:
            for i in range(1, 8):
                new_pos = (row + i * d_row, col + i * d_col)
                if not board.is_within_bounds(new_pos):
                    break
                target_piece = board.get_piece_at(new_pos)
                if target_piece:
                    if target_piece.color != self.color:
                        moves.append((self.position, new_pos))
                    break
                moves.append((self.position, new_pos))
        return moves

    def get_knight_moves(self, board):
        moves = []
        row, col = self.position
        jumps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for d_row, d_col in jumps:
            new_pos = (row + d_row, col + d_col)
            if board.is_within_bounds(new_pos) and (
                not board.get_piece_at(new_pos)
                or board.get_piece_at(new_pos).color != self.color
            ):
                moves.append((self.position, new_pos))
        return moves

    def get_squire_moves(self, board):
        moves = []
        row, col = self.position
        potential_moves = [
            (row + d_row, col + d_col)
            for d_row in range(-2, 3)
            for d_col in range(-2, 3)
            if abs(d_row) + abs(d_col) == 2
        ]
        for new_pos in potential_moves:
            if board.is_within_bounds(new_pos) and (
                not board.get_piece_at(new_pos)
                or board.get_piece_at(new_pos).color != self.color
            ):
                moves.append((self.position, new_pos))
        return moves

    def get_combatant_moves(self, board):
        moves = []
        row, col = self.position
        ortho_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diag_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d_row, d_col in ortho_directions:
            new_pos = (row + d_row, col + d_col)
            if board.is_within_bounds(new_pos) and not board.get_piece_at(new_pos):
                moves.append((self.position, new_pos))
        for d_row, d_col in diag_directions:
            new_pos = (row + d_row, col + d_col)
            target_piece = board.get_piece_at(new_pos)
            if (
                board.is_within_bounds(new_pos)
                and target_piece
                and target_piece.color != self.color
            ):
                moves.append((self.position, new_pos))
        return moves


class Board:
    def __init__(self, gameboard):
        self.gameboard = self.create_board(gameboard)

    def create_board(self, pieces):
        board = {}
        for piece_data in pieces:
            if isinstance(piece_data, tuple) and len(piece_data) == 3:
                piece_type, color, position = piece_data
                piece = Piece(piece_type, color, position)
                board[position] = piece
            else:
                continue
        return board

    def get_piece_at(self, position):
        return self.gameboard.get(position, None)

    def move_piece(self, start_pos, end_pos):
        piece = self.gameboard.pop(start_pos, None)
        captured_piece = self.gameboard.get(end_pos)
        self.gameboard[end_pos] = piece
        piece.position = end_pos
        return captured_piece

    def undo_move(self, start_pos, end_pos, captured_piece):
        piece = self.gameboard.pop(end_pos)
        self.gameboard[start_pos] = piece
        piece.position = start_pos
        if captured_piece:
            self.gameboard[end_pos] = captured_piece

    def is_within_bounds(self, position):
        return 0 <= position[0] < 8 and 0 <= position[1] < 8

    def is_game_over(self):
        pieces = list(self.gameboard.values())
        kings_only = all(piece.piece_type == "King" for piece in pieces)
        return kings_only


def get_legal_moves(gameboard, color):
    board = Board(gameboard)
    moves = []
    for position, piece in board.gameboard.items():
        if piece.color == color:
            moves.extend(piece.get_moves(board))
    return moves


def evaluate_board(board):
    score = 0
    for piece in board.gameboard.values():
        if piece.color == "white":
            score += piece_value(piece)
        else:
            score -= piece_value(piece)
    return score


def piece_value(piece):
    values = {
        "King": 1000,
        "Rook": 5,
        "Bishop": 3,
        "Knight": 3,
        "Squire": 2,
        "Combatant": 1,
    }
    return values.get(piece.piece_type, 0)


def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    legal_moves = get_legal_moves(
        board.gameboard, "white" if maximizing_player else "black"
    )
    best_move = None

    if maximizing_player:
        max_eval = float("-inf")
        for move in legal_moves:
            start_pos, end_pos = move
            captured_piece = board.move_piece(start_pos, end_pos)

            eval, _ = alpha_beta_pruning(board, depth - 1, alpha, beta, False)
            board.undo_move(start_pos, end_pos, captured_piece)

            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval, best_move

    else:
        min_eval = float("inf")
        for move in legal_moves:
            start_pos, end_pos = move
            captured_piece = board.move_piece(start_pos, end_pos)

            eval, _ = alpha_beta_pruning(board, depth - 1, alpha, beta, True)
            board.undo_move(start_pos, end_pos, captured_piece)

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval, best_move


def studentAgent(gameboard):
    board = Board(gameboard)
    _, best_move = alpha_beta_pruning(
        board, depth=3, alpha=float("-inf"), beta=float("inf"), maximizing_player=True
    )
    return best_move
