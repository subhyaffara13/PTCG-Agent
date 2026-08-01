
def _triangular_solve_batching_rule(
    axis_data, batched_args, batch_dims, *, left_side, lower, transpose_a, conjugate_a,
    unit_diagonal):
  x, y = batched_args
  bx, by = batch_dims
  if bx is None and by is None:
    out = triangular_solve(x, y, left_side=left_side, lower=lower,
                           transpose_a=transpose_a, conjugate_a=conjugate_a,
                           unit_diagonal=unit_diagonal)
    return out, None
  if bx is None:
    if left_side:
      y = batching.moveaxis(y, by, -1)
      y_flat = y.reshape(y.shape[:-2] + (y.shape[-2] * y.shape[-1],))
      bdim_out = y.ndim - 1
    else:
      y = batching.moveaxis(y, by, -2)
      y_flat = y.reshape(y.shape[:-3]  + (y.shape[-3] * y.shape[-2], y.shape[-1]))
      bdim_out = y.ndim - 2
    out_flat = triangular_solve(
        x, y_flat, left_side=left_side, lower=lower,
        transpose_a=transpose_a, conjugate_a=conjugate_a,
        unit_diagonal=unit_diagonal)
    return out_flat.reshape(y.shape), bdim_out
  else:
    x = batching.bdim_at_front(x, bx, axis_data.size, axis_data.explicit_mesh_axis)
    y = batching.bdim_at_front(y, by, axis_data.size, axis_data.explicit_mesh_axis)
    return triangular_solve(x, y, left_side=left_side, lower=lower,
                            transpose_a=transpose_a, conjugate_a=conjugate_a,
                            unit_diagonal=unit_diagonal), 0

