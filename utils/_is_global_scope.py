
def _is_global_scope(collective_axes: CollectiveAxesType,
                     axis_names: _AxisNames):
  """Returns whether the collective axes represents a GPU global scope."""
  return set(collective_axes) == set(axis_names)

