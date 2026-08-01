
def _coo_extract(row: Array, col: Array, mat: Array) -> Array:
  """Extract values of dense matrix mat at given COO indices."""
  return mat[row, col]

