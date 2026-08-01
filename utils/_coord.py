
def _coord(move):
  """Returns (row, col) from an action id."""
  return (move // _NUM_COLS, move % _NUM_COLS)

