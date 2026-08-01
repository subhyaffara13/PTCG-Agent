
def mask_variable_updates(
    current_tree: A,
    snapshot_tree: A,
    *,
    prefix: tp.Any = Missing,
    keep_fn: KeepFn | None = None,
) -> A:
  if keep_fn is None:
    keep_fn = lambda _, _pfx, cur, snap: variable_changed(cur, snap)

  def _mask_updates(path, prefix_leaf, current, snapshot):
    if isinstance(current, variablelib.Variable):
      if current.hijax or current.ref:
        return Mask()
      if keep_fn(path, prefix_leaf, current, snapshot):
        return current
    return Mask()
  prefix_leaf = lambda x: x is None
  is_leaf = lambda x: isinstance(x, variablelib.Variable)
  if prefix is Missing:
    return jax.tree.map_with_path(
        lambda path, cur, snap: _mask_updates(path, None, cur, snap),
        current_tree, snapshot_tree, is_leaf=is_leaf
    )
  return broadcast_prefix_map(
      _mask_updates, prefix, current_tree, snapshot_tree, is_leaf=is_leaf,
      prefix_leaf=prefix_leaf,
  )

