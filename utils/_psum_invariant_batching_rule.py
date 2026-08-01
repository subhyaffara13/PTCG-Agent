
def _psum_invariant_batching_rule(axis_data, vals_in, dims_in, axes):
  return _batched_reduction_collective(
      psum_invariant_p, lambda v, axis_size: axis_size * v,
      axis_data, vals_in, dims_in, axes, None)

