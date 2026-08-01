
def _canonicalize_axis_index_groups(axis_index_groups):
  if axis_index_groups is None:
    return
  return tuple(map(tuple, axis_index_groups))

