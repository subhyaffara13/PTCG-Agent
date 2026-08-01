
def _all_gather_reduced_transpose_rule(
    cts, x, *, all_gather_dimension, axis_name, axis_size, tiled):
  return (unreduced_psum_scatter(cts, axis_name=axis_name,
                                 scatter_dimension=all_gather_dimension,
                                 tiled=tiled),)

