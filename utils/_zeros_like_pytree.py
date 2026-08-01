
def _zeros_like_pytree(x):
  return tree_map(p2tz, x)

