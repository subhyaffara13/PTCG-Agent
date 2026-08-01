
def _move_axis(move_fn, axes, tree):
  def move_axis_leaf(path, ax, leaf):
    assert isinstance(ax, int)
    if ax != 0:
      return move_fn(ax, leaf)
    return leaf

  return extract.broadcast_prefix_map(
      move_axis_leaf, axes, tree, prefix_leaf=lambda x: x is None
  )

