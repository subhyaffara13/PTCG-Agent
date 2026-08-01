
def nfold_vmap(fun, N, *, broadcasted=True, in_axes=0):
  """Convenience function to apply (broadcasted) vmap N times."""
  _vmap = broadcasting_vmap if broadcasted else vmap
  for _ in range(N):
    fun = _vmap(fun, in_axes=in_axes)
  return fun

