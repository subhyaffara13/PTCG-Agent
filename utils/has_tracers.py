
def has_tracers(tree: pytypes.ArrayTree) -> bool:
  """Checks whether a tree contains any tracers."""
  return any(
      isinstance(x, jax.core.Tracer) for x in jax.tree_util.tree_leaves(tree))

