
def todense(arr: JAXSparse | Array) -> Array:
  """Convert input to a dense matrix. If input is already dense, pass through."""
  bufs, tree = tree_util.tree_flatten(arr)
  return todense_p.bind(*bufs, tree=tree)

