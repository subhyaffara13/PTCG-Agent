
def _replica_groups(axis_ctx, axis_name, axis_index_groups):
  replica_groups = pxla.axis_groups(axis_ctx, axis_name)
  if axis_index_groups is not None:
    replica_groups = [[axis_group[i] for i in axis_index_group]
                      for axis_group in replica_groups
                      for axis_index_group in axis_index_groups]
  return replica_groups

