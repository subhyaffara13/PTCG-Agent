
def tree_broadcast(prefix_tree: Any, full_tree: Any,
                   is_leaf: Callable[[Any], bool] | None = None
                  ) -> Any:
  """Alias of :func:`jax.tree.broadcast`."""
  broadcast_leaves = broadcast_prefix(prefix_tree, full_tree, is_leaf=is_leaf)
  return tree_structure(full_tree).unflatten(broadcast_leaves)

