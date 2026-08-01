
def _even_easier_create_game():
  """Leave out the names too, if you prefer."""
  return pyspiel.create_matrix_game([[-1, 1], [1, -1]], [[1, -1], [-1, 1]])

