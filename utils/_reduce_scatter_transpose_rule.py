
def _reduce_scatter_transpose_rule(cts, x, *, axis_name, scatter_dimension,
                                   axis_index_groups, axis_size, tiled):
  return (all_gather(cts, axis_name=axis_name,
                     axis_index_groups=axis_index_groups,
                     axis=scatter_dimension, tiled=tiled),)

