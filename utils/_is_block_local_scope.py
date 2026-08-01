
def _is_block_local_scope(collective_axes: CollectiveAxesType,
                          axis_names: _AxisNames):
  """Returns whether the collective axes represents a block scope."""
  if axis_names.wg is None:
    return not collective_axes
  else:
    return collective_axes == (axis_names.wg,)

