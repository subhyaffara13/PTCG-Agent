
def _tuple_all_binop(binop, xs, ys):
  """Dynamic reduce_all calculation with a user-provided comparison op."""
  differences = jax.tree.leaves(jax.tree.map(lambda x, y: binop(x, y), xs, ys))
  return functools.reduce(lambda x, y: x & y, differences, True)

