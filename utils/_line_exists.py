
def _line_exists(board):
  """Checks if a line exists, returns "x" or "o" if so, and None otherwise."""
  return (_line_value(board[0]) or _line_value(board[1]) or
          _line_value(board[2]) or _line_value(board[:, 0]) or
          _line_value(board[:, 1]) or _line_value(board[:, 2]) or
          _line_value(board.diagonal()) or
          _line_value(np.fliplr(board).diagonal()))

