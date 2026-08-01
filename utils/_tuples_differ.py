
def _tuples_differ(xs, ys):
  """Dynamic index-tuple comparison calculation."""
  differences = jax.tree.leaves(jax.tree.map(lambda x, y: x != y, xs, ys))
  return functools.reduce(lambda x, y: x | y, differences, False)

