
def get_tracers(tree: pytypes.ArrayTree) -> Tuple[jax.core.Tracer]:
  """Returns a tuple with tracers from a tree."""
  return tuple(
      x for x in jax.tree_util.tree_leaves(tree)
      if isinstance(x, jax.core.Tracer))

