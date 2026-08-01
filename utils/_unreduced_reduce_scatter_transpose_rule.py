
def _unreduced_reduce_scatter_transpose_rule(
    cts, x, *, axis_name, scatter_dimension, axis_size, tiled):
  return (all_gather_reduced(cts, axis_name=axis_name, axis=scatter_dimension,
                             tiled=tiled),)

