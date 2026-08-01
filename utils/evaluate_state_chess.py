
def evaluate_state_chess(state: pyspiel.State, player: int):
  """Evaluates the given state."""
  board = state.board()
  value = 0
  for row in range(8):
    for col in range(8):
      square = pyspiel.chess.Square(row, col)
      piece = board.at(square)
      if piece.type == pyspiel.chess.PieceType.EMPTY:
        continue
      elif piece.type == pyspiel.chess.PieceType.PAWN:
        piece_val = 1
      elif piece.type == pyspiel.chess.PieceType.KNIGHT:
        piece_val = 3
      elif piece.type == pyspiel.chess.PieceType.BISHOP:
        piece_val = 3
      elif piece.type == pyspiel.chess.PieceType.ROOK:
        piece_val = 5
      elif piece.type == pyspiel.chess.PieceType.QUEEN:
        piece_val = 9
      elif piece.type == pyspiel.chess.PieceType.KING:
        piece_val = 0
      else:
        raise ValueError(f"Unknown piece type: {piece.piece_type}")
      # note that white is 1, black is 0
      if ((piece.color == pyspiel.chess.Color.WHITE and player == 1) or
          (piece.color == pyspiel.chess.Color.BLACK and player == 0)):
        value += piece_val
      else:
        value -= piece_val
  return value

