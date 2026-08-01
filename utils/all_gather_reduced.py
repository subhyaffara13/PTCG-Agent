
def all_gather_reduced(x, axis_name, *, axis: int = 0, tiled: bool = False, is_async: bool = False):
  if not isinstance(axis_name, tuple):
    axis_name = (axis_name,)
  if not axis_name:
    return x
  axis_size = _axis_size(axis_name, None)
  def bind(leaf):
    prim = all_gather_reduced_start_p if is_async else all_gather_reduced_p
    return prim.bind(
        leaf,
        all_gather_dimension=canonicalize_axis(
            axis, np.ndim(leaf) if tiled else np.ndim(leaf) + 1),
        axis_name=axis_name, axis_size=axis_size, tiled=tiled)
  return tree_util.tree_map(bind, x)

