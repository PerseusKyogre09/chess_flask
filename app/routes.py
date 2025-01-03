from flask import Blueprint, render_template, jsonify, request
import chess
from app.models import ChessBoard

main = Blueprint('main', __name__)

# Initialize chess_game here
chess_game = ChessBoard()

@main.route('/')
def index():
    board = chess_game.get_board()
    board_fen=board.fen()
    return render_template('chess.html', board=board, chess=chess, board_fen=board_fen)

@main.route('/move', methods=['POST'])
def move():
    data = request.json
    from_pos = data['from']
    to_pos = data['to']

    success, message = chess_game.move_piece(from_pos, to_pos)
    if success:
        game_over, status = chess_game.is_game_over()
        if game_over:
            return jsonify({'success': True, 'message': status, 'game_over': True})
        else:
            chess_game.ai_move()
            game_over, status = chess_game.is_game_over()
            if game_over:
                return jsonify({'success': True, 'message': status, 'game_over': True})
    return jsonify({'success': success, 'message': message})

@main.route('/valid-moves', methods=['POST'])
def valid_moves():
    data = request.json
    pos = data['pos']
    valid_moves = chess_game.get_valid_moves(pos)
    return jsonify({'valid_moves': valid_moves})
