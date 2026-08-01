
def _format_matrix(mat):
  return np.char.array([_format_vec(row) for row in mat])

