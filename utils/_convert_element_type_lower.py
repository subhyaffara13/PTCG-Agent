
def _convert_element_type_lower(ctx, operand, *, new_dtype, weak_type,
                                sharding):
  aval_in, = ctx.avals_in
  aval_out, = ctx.avals_out
  if (dtypes.issubdtype(aval_in.dtype, np.complexfloating) and
      not dtypes.issubdtype(new_dtype, np.complexfloating)):
    operand = hlo.real(operand)
    aval_in = aval_in.update(dtype=_real_dtype(aval_in.dtype))
  out = mlir.convert_hlo(ctx, operand, aval_in, aval_out)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

