
def _shapes(pytree):
  return map(np.shape, tree_leaves(pytree))

