
def _apply_axis_fn(
    tree: tp.Any,
    axes: tp.Any,
    metadata: tp.Mapping[str, tp.Any],
    axis_fn: tp.Callable[..., tp.Any],
) -> None:
  prefix_leaf = lambda x: x is None
  is_leaf = lambda x: isinstance(x, variablelib.Variable)
  def apply_fn(path, axis, leaf):
    if isinstance(axis, int) and isinstance(leaf, variablelib.Variable):
      axis_fn(leaf, axis, metadata)

  extract.broadcast_prefix_map(apply_fn, axes, tree, is_leaf=is_leaf, prefix_leaf=prefix_leaf)

