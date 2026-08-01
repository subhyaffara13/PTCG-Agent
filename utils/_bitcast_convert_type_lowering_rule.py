
def _bitcast_convert_type_lowering_rule(
    ctx: LoweringRuleContext, x, *, new_dtype
):
  (in_aval, ) = ctx.avals_in
  (out_aval,) = ctx.avals_out
  out_type = ctx.aval_to_ir_type(out_aval)
  old_bitwidth = dtypes.itemsize_bits(in_aval.dtype)
  new_bitwidth = dtypes.itemsize_bits(new_dtype)
  if old_bitwidth != new_bitwidth:
    raise NotImplementedError("Changing bitwidths not supported.")
  if in_aval.shape:
    return tpu.bitcast(out_type, x)
  return arith.bitcast(out_type, x)


def _bitcast_convert_type_lowering_rule(
    ctx: LoweringRuleContext, x, *, new_dtype
):
  [x_aval] = ctx.avals_in
  src_elem_type = mgpu_utils.dtype_to_ir_type(x_aval.dtype)
  dst_elem_type = mgpu_utils.dtype_to_ir_type(new_dtype)
  assert isinstance(src_elem_type, (ir.IntegerType, ir.FloatType))
  assert isinstance(dst_elem_type, (ir.IntegerType, ir.FloatType))
  if src_elem_type.width != dst_elem_type.width:
    raise NotImplementedError(
        f"Cannot bitcast from {x_aval.dtype} to {new_dtype} because they"
        " have different widths"
    )

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    x = _ensure_ir_value(x, x_aval.dtype)
    return arith_dialect.bitcast(
        ir.VectorType.get(x_aval.shape, dst_elem_type), x
    )

  x = _ensure_fa(x, x_aval.dtype)
  output_is_signed = mgpu_utils.is_signed(new_dtype)
  return mgpu.FragmentedArray.bitcast(
      x, dst_elem_type, output_is_signed=output_is_signed
  )


def _bitcast_convert_type_lowering_rule(
    ctx: LoweringRuleContext, operand: ir.Value, *, new_dtype
) -> ir.Value:
  # TODO(petebu) Handle case where src and dst types have different bitwidths
  src_elem_type = _element_type(operand.type)
  dst_elem_type = _element_type(_dtype_to_ir_type(new_dtype))
  assert isinstance(src_elem_type, (ir.IntegerType, ir.FloatType))
  assert isinstance(dst_elem_type, (ir.IntegerType, ir.FloatType))
  if src_elem_type.width != dst_elem_type.width:
    raise NotImplementedError(
        f"cannot cast {operand} to {new_dtype} because of different widths"
    )
  if isinstance(operand.type, ir.RankedTensorType):
    shape = ir.RankedTensorType(operand.type).shape
    result_type = ir.RankedTensorType.get(shape, dst_elem_type)
  else:
    result_type = dst_elem_type
  return tt_dialect.bitcast(result_type, operand)

