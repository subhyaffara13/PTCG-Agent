
def _all_gather_invariant_batched_collective(
    axis_data, vals_in, dims_in, all_gather_dimension, axis_name, axis_size,
    tiled):
  return _all_gather_batched_collective(
      all_gather_invariant_p, axis_data, vals_in, dims_in, all_gather_dimension,
      axis_name, None, axis_size, tiled)

