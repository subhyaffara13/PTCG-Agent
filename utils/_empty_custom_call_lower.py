
def _empty_custom_call_lower(ctx, *, shape, dtype, out_sharding):
  if not core.is_constant_shape(shape):
    return _empty_lower(ctx, shape=shape, dtype=dtype, out_sharding=out_sharding)
  dtype = dtype if dtypes.issubdtype(dtype, dtypes.extended) else np.dtype(dtype)
  aval_out = core.ShapedArray(shape, dtype, sharding=out_sharding)
  phys_aval = core.physical_aval(aval_out)
  custom_call_op = hlo.CustomCallOp(
      [mlir.ir.RankedTensorType.get(
          list(phys_aval.shape), mlir.dtype_to_ir_type(phys_aval.dtype))],
      [],
      call_target_name=mlir.ir.StringAttr.get("AllocateBuffer"),
      has_side_effect=mlir.ir.BoolAttr.get(False),
  )
  assert len(custom_call_op.results) == 1
  res = custom_call_op.results[0]
  return [mlir.lower_with_sharding_in_types(ctx, res, phys_aval)]

