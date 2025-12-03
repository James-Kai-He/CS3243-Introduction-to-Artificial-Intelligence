from typing import Tuple, List, Literal, Optional


class Piece:
    def __init__(
        self,
        piece_type: str,
        color: Literal["white", "black"],
        position: Tuple[int, int],
    ):
        self.piece_type = piece_type
        self.color = color
        self.position = position

    def get_value(self) -> int:
        values = {
            "King": 1000,
            "Rook": 5,
            "Bishop": 3,
            "Knight": 3,
            "Squire": 2,
            "Combatant": 1,
        }
        return values.get(self.piece_type, 0)

    def get_moves(self, board):
        if self.piece_type == "King":
            return self.get_king_moves(board)
        elif self.piece_type == "Rook":
            return self.get_rook_moves(board)
        elif self.piece_type == "Bishop":
            return self.get_bishop_moves(board)
        elif self.piece_type == "Knight":
            return self.get_knight_moves(board)
        elif self.piece_type == "Squire":
            return self.get_squire_moves(board)
        elif self.piece_type == "Combatant":
            return self.get_combatant_moves(board)
        return []

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
    def __init__(self, pieces: List[Piece]):
        self.pieces = pieces

    def is_king_captured(self, color: Literal["white", "black"]) -> bool:
        for piece in self.pieces:
            if piece.piece_type == "King" and piece.color == color:
                return False
        return True

    def calculate_material_score(self) -> int:
        score = 0
        for piece in self.pieces:
            score += piece.get_value()
        return score

    def generate_all_legal_moves(
        self, color: Literal["white", "black"]
    ) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        moves = []
        for piece in self.pieces:
            if piece.color == color:
                moves.extend(piece.get_moves(self))
        return moves

    def is_within_bounds(self, position: Tuple[int, int]) -> bool:
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece_at(self, position: Tuple[int, int]) -> Optional[Piece]:
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def make_move(self, move: Tuple[Tuple[int, int], Tuple[int, int]]):
        start, end = move
        piece = self.get_piece_at(start)
        if piece:
            self.pieces.remove(piece)
            piece.position = end
            target = self.get_piece_at(end)
            if target:
                self.pieces.remove(target)
            self.pieces.append(piece)

    def copy(self):
        return Board(
            [
                Piece(piece.piece_type, piece.color, piece.position)
                for piece in self.pieces
            ]
        )


class State:
    def __init__(self, board: Board, current_turn: Literal["white", "black"]):
        self.board = board
        self.current_turn = current_turn

    def is_terminal(self) -> bool:
        return self.board.is_king_captured("white") or self.board.is_king_captured(
            "black"
        )

    def evaluate(self) -> int:
        if self.board.is_king_captured("black"):
            return float("inf")  # White wins
        elif self.board.is_king_captured("white"):
            return float("-inf")  # Black wins
        else:
            return self.board.calculate_material_score()

    def apply_move(self, move: Tuple[Tuple[int, int], Tuple[int, int]]):
        new_board = self.board.copy()
        new_board.make_move(move)
        return State(new_board, "black" if self.current_turn == "white" else "white")


def studentAgent(
    gameboard: List[Tuple[str, str, Tuple[int, int]]]
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    board = setUpBoard(gameboard)
    initial_state = State(board, current_turn="white")
    _, best_move = ab(
        initial_state,
        depth=3,
        alpha=float("-inf"),
        beta=float("inf"),
        maximizing_player=True,
    )
    return best_move


def get_legal_moves(
    gameboard: List[Tuple[str, str, Tuple[int, int]]], color: Literal["white", "black"]
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    board = setUpBoard(gameboard)
    return board.generate_all_legal_moves(color)


def ab(
    state: State, depth: int, alpha: float, beta: float, maximizing_player: bool
) -> Tuple[int, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    if depth == 0 or state.is_terminal():
        return state.evaluate(), None

    best_move = None
    if maximizing_player:
        max_eval = float("-inf")
        for move in state.board.generate_all_legal_moves("white"):
            new_state = state.apply_move(move)
            eval, _ = ab(new_state, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = float("inf")
        for move in state.board.generate_all_legal_moves("black"):
            new_state = state.apply_move(move)
            eval, _ = ab(new_state, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def setUpBoard(gameboard: List[Tuple[str, str, Tuple[int, int]]]) -> Board:
    pieces = [
        Piece(piece_type, color, position) for piece_type, color, position in gameboard
    ]
    return Board(pieces)
