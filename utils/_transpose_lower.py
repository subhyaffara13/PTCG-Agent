
def _transpose_lower(ctx, x, *, permutation):
  aval_out, = ctx.avals_out
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    elt_shape = core.physical_element_aval(aval_out.dtype).shape
    trailing_dims = [aval_out.ndim + i for i in range(len(elt_shape))]
    permutation = [*permutation, *trailing_dims]
  out = hlo.transpose(x, mlir.dense_int_array(permutation))
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

