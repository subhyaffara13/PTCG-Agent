
def _unreduced_reduce_scatter_lowering(
    prim, ctx, x, *, axis_name, scatter_dimension, axis_size, tiled):
  return _reduce_scatter_lowering(
      prim, ctx, x, axis_name=axis_name, scatter_dimension=scatter_dimension,
      axis_size=axis_size, tiled=tiled, axis_index_groups=None)

