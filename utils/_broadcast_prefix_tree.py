
def _broadcast_prefix_tree(prefix_tree: Any, full_tree: Any) -> list[Any]:
  bcast_flat = []
  num_leaves_fn = lambda t: jax.tree.flatten(t)[1].num_leaves
  jax.tree.map(
      lambda x, subtree: bcast_flat.extend([x] * num_leaves_fn(subtree)),
      prefix_tree,
      full_tree,
      is_leaf=lambda x: x is None,
  )
  return bcast_flat

