
def tree_reduce_associative(
    operation: Callable[[T, T], T],
    tree: Any,
    *,
    identity: T | Unspecified = Unspecified(),
    is_leaf: Callable[[Any], bool] | None = None,
) -> T:
  """Alias of :func:`jax.tree.reduce_associative`."""
  sequence = tree_leaves(tree, is_leaf=is_leaf)
  return _parallel_reduce(sequence, operation, identity)

