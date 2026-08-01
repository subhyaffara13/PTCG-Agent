
def _normalize_tree(x):
  # divide by the L2 norm of the tree weights.
  return optax.tree.scale(1.0 / optax.tree.norm(x), x)

