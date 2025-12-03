from typing import List, Tuple, Union, Optional

class Piece:
    def __init__(self, name: str, color: str, position: Tuple[int, int]):
        self.name = name
        self.color = color
        self.position = position

    def get_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        row, col = self.position
        moves = []
        
        if self.name == "King":
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions:
                new_pos = (row + dr, col + dc)
                if board.is_within_bounds(new_pos) and (board.get_piece_at(new_pos) is None or board.get_piece_at(new_pos).color != self.color):
                    moves.append(new_pos)

        elif self.name == "Rook":
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                for i in range(1, 8):
                    new_pos = (row + dr * i, col + dc * i)
                    if not board.is_within_bounds(new_pos):
                        break
                    target = board.get_piece_at(new_pos)
                    if target is None:
                        moves.append(new_pos)
                    elif target.color != self.color:
                        moves.append(new_pos)
                        break
                    else:
                        break

        elif self.name == "Bishop":
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                for i in range(1, 8):
                    new_pos = (row + dr * i, col + dc * i)
                    if not board.is_within_bounds(new_pos):
                        break
                    target = board.get_piece_at(new_pos)
                    if target is None:
                        moves.append(new_pos)
                    elif target.color != self.color:
                        moves.append(new_pos)
                        break
                    else:
                        break

        elif self.name == "Knight":
            knight_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
            for dr, dc in knight_moves:
                new_pos = (row + dr, col + dc)
                if board.is_within_bounds(new_pos) and (board.get_piece_at(new_pos) is None or board.get_piece_at(new_pos).color != self.color):
                    moves.append(new_pos)

        elif self.name == "Squire":
            squire_moves = [(2, 0), (0, 2), (-2, 0), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in squire_moves:
                new_pos = (row + dr, col + dc)
                if board.is_within_bounds(new_pos) and (board.get_piece_at(new_pos) is None or board.get_piece_at(new_pos).color != self.color):
                    moves.append(new_pos)

        elif self.name == "Combatant":
            orthogonal_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            diagonal_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            
            for dr, dc in orthogonal_moves:
                new_pos = (row + dr, col + dc)
                if board.is_within_bounds(new_pos) and board.get_piece_at(new_pos) is None:
                    moves.append(new_pos)
            
            for dr, dc in diagonal_moves:
                new_pos = (row + dr, col + dc)
                if board.is_within_bounds(new_pos):
                    target = board.get_piece_at(new_pos)
                    if target and target.color != self.color:
                        moves.append(new_pos)

        return moves


class Board:
    def __init__(self, gameboard: List[Tuple[str, str, Tuple[int, int]]]):
        self.board = {}
        for piece_info in gameboard:
            name, color, position = piece_info
            self.board[position] = Piece(name, color, position)

    def get_piece_at(self, position: Tuple[int, int]) -> Optional[Piece]:
        return self.board.get(position)

    def move_piece(self, start: Tuple[int, int], end: Tuple[int, int]):
        piece = self.board.pop(start, None)
        if piece:
            piece.position = end
            self.board[end] = piece

    def is_within_bounds(self, position: Tuple[int, int]) -> bool:
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8

    def get_all_pieces(self, color: str) -> List[Piece]:
        return [piece for piece in self.board.values() if piece.color == color]


class State:
    def __init__(self, board: Board, current_turn: str):
        self.board = board
        self.current_turn = current_turn
        self.opponent_color = 'black' if current_turn == 'white' else 'white'

    def evaluate(self) -> int:
        piece_values = {
            "King": 1000, "Queen": 9, "Rook": 5, "Bishop": 3, "Knight": 3, 
            "Squire": 2, "Combatant": 1
        }
        value = 0
        for piece in self.board.board.values():
            piece_value = piece_values.get(piece.name, 0)
            if piece.color == "white":
                value += piece_value
            else:
                value -= piece_value
        return value

    def get_legal_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        moves = []
        for piece in self.board.get_all_pieces(self.current_turn):
            piece_moves = piece.get_moves(self.board)
            for move in piece_moves:
                moves.append((piece.position, move))
        return moves


def get_legal_moves(gameboard: List[Tuple[str, str, Tuple[int, int]]], color: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    board = Board(gameboard)
    state = State(board, color)
    return state.get_legal_moves()


def alpha_beta(state: State, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    if depth == 0 or not state.get_legal_moves():
        return state.evaluate(), None
    
    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for move in state.get_legal_moves():
            start, end = move
            new_board = Board([(p.name, p.color, p.position) for p in state.board.board.values()])
            new_board.move_piece(start, end)
            new_state = State(new_board, 'black')
            eval_score, _ = alpha_beta(new_state, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for move in state.get_legal_moves():
            start, end = move
            new_board = Board([(p.name, p.color, p.position) for p in state.board.board.values()])
            new_board.move_piece(start, end)
            new_state = State(new_board, 'white')
            eval_score, _ = alpha_beta(new_state, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def studentAgent(gameboard: List[Tuple[str, str, Tuple[int, int]]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    board = Board(gameboard)
    state = State(board, "white")
    _, best_move = alpha_beta(state, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True)
    return best_move if best_move else ((0, 0), (0, 0))
