
def _reduce_scatter_batcher(vals_in, dims_in, *, scatter_dimension, axis_name,
                            axis_index_groups, axis_size, tiled):
  (x,), (d,) = vals_in, dims_in
  if d <= scatter_dimension:
    scatter_dimension += 1
  elif not tiled:  # Tiled all-scatter doesn't change the rank
    d += 1
  result = reduce_scatter_p.bind(
      x,
      scatter_dimension=scatter_dimension,
      axis_name=axis_name,
      axis_index_groups=axis_index_groups,
      axis_size=axis_size,
      tiled=tiled)
  return result, d

