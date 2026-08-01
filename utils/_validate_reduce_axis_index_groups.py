
def _validate_reduce_axis_index_groups(axis_index_groups):
  if axis_index_groups is None:
    return
  axis_space = range(sum(len(group) for group in axis_index_groups))
  if {i for g in axis_index_groups for i in g} != set(axis_space):
    raise ValueError("axis_index_groups must cover all indices exactly once")

