
def _opaque_comparison_hlo(direction, reduction_op, identity, ctx,
                           avals_in, aval_out, x, y):
  aval_x, aval_y = avals_in
  base_aval_x = core.physical_aval(aval_x)
  base_aval_y = core.physical_aval(aval_y)
  base_aval_out = core.ShapedArray(base_aval_x.shape, aval_out.dtype)  # pyrefly: ignore[missing-attribute]
  reduce_axes = tuple(range(aval_out.ndim, base_aval_out.ndim))
  res, = mlir.delegate_lowering(
      ctx, partial(_compare_lower_hlo, direction, False),
      x, y, avals_in=[base_aval_x, base_aval_y], avals_out=[base_aval_out])
  return mlir.delegate_lowering(
      ctx, partial(_unary_reduce_lower, reduction_op, identity,
                   axes=reduce_axes),
      res, avals_in=[base_aval_out], avals_out=[aval_out])

