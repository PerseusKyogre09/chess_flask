import chess
import chess.engine
import os

class ChessBoard:
    def __init__(self):
        self.board = chess.Board()
        stockfish_path = os.path.join(os.path.dirname(__file__), 'static', 'stockfish', 'stockfish-windows-x86-64-avx2')
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def get_board(self):
        return self.board

    def move_piece(self, from_pos, to_pos):
        try:
            # Adjusting for board orientation
            # from_pos and to_pos are given as (row, col)
            from_square = chess.square(from_pos[1], 7 - from_pos[0])  # Adjust row for chess library
            to_square = chess.square(to_pos[1], 7 - to_pos[0])        # Adjust row for chess library
            move = chess.Move(from_square, to_square)
            
            if move in self.board.legal_moves:
                self.board.push(move)
                return True, "Move successful."
            else:
                return False, "Illegal move."
        except Exception as e:
            return False, str(e)


    def ai_move(self):
        if not self.board.is_game_over():
            result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
            self.board.push(result.move)
            return True, "AI moved successfully."
        return False, "Game over."

    def get_valid_moves(self, pos):
        square = chess.square(pos[1], 7 - pos[0])  # Adjust for orientation
        return [(move.to_square // 8, 7 - (move.to_square % 8)) for move in self.board.legal_moves if move.from_square == square]


    def is_game_over(self):
        if self.board.is_checkmate():
            return True, "Checkmate!"
        if self.board.is_stalemate():
            return True, "Stalemate!"
        if self.board.is_insufficient_material():
            return True, "Draw due to insufficient material."
        return False, ""
