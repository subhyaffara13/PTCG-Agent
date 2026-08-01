
def _copy_params(params):
  """Returns a copy of the params."""
  return jax.tree_util.tree_map(lambda x: x.copy(), params)

