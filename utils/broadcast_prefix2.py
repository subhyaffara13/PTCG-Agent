
def broadcast_prefix2(
  prefix_tree: tp.Any,
  full_tree: tp.Any,
  is_leaf: tp.Callable[[tp.Any], bool] | None = None,
  prefix_leaf: tp.Callable[[tp.Any], bool] | None = None,
) -> tuple[list[KeyPath], list[tp.Any]]:
  _prefix_leaf: tp.Callable[[tp.Any], bool] | None
  if prefix_leaf is not None and is_leaf is not None:
    _prefix_leaf = lambda x: prefix_leaf(x) or is_leaf(x)
  elif prefix_leaf is not None:
    _prefix_leaf = prefix_leaf
  else:
    _prefix_leaf = is_leaf

  paths: list[KeyPath] = []
  leaves: list[tp.Any] = []
  num_leaves = lambda t: jax.tree.structure(t, is_leaf=is_leaf).num_leaves
  def add_leaves(path, x, subtree):
    n = num_leaves(subtree)
    paths.extend([path] * n)
    leaves.extend([x] * n)
  jax.tree.map_with_path(add_leaves, prefix_tree, full_tree, is_leaf=_prefix_leaf)
  return paths, leaves

