
def _norm(x):
  xs = tree_leaves(x)
  return jnp.sqrt(sum(map(_vdot_real_part, xs, xs)))

