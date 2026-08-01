
def _empty_lower(ctx, *, shape, dtype, out_sharding):
  dtype = dtype if dtypes.issubdtype(dtype, dtypes.extended) else np.dtype(dtype)
  aval_out = core.ShapedArray(shape, dtype, sharding=out_sharding)
  phys_aval = core.physical_aval(aval_out)
  out = mlir.ir_constant(np.zeros((), phys_aval.dtype))
  out = mlir.broadcast_in_dim(ctx, out, phys_aval, broadcast_dimensions=[])
  return [mlir.lower_with_sharding_in_types(ctx, out, phys_aval)]

