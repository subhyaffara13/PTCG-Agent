
def _all_gather_transpose_rule(cts, x, *, all_gather_dimension, axis_name,
                               axis_index_groups, axis_size, tiled):
  return (psum_scatter(cts, axis_name=axis_name,
                       scatter_dimension=all_gather_dimension,
                       axis_index_groups=axis_index_groups,
                       tiled=tiled),)

