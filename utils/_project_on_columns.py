
def _project_on_columns(A, v):
  """
  Returns A.T.conj() @ v.
  """
  v_proj = tree_map(
      lambda X, y: _einsum("...n,...->n", X.conj(), y), A, v,
  )
  return tree_reduce(operator.add, v_proj)

