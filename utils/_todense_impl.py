
def _todense_impl(*bufs, tree):
  arr = tree_util.tree_unflatten(tree, bufs)
  return arr.todense() if isinstance(arr, JAXSparse) else arr

