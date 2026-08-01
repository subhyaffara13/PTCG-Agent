
def _tree_map_axes(fn, tree):
  """Only map over AxisMetadata leaves in pytree - identity for other leaves."""
  safe_fn = lambda x: fn(x) if isinstance(x, AxisMetadata) else x
  return jax.tree_util.tree_map(
      safe_fn, tree, is_leaf=lambda x: isinstance(x, AxisMetadata)
  )

