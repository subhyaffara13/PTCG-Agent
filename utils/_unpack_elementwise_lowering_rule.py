
def _unpack_elementwise_lowering_rule(
    ctx: LoweringRuleContext, x, index, packed_dtype, unpacked_dtype
):
  in_aval = ctx.avals_in[0]
  out_type = ir.VectorType.get(
      ctx.lowering_context.dynamic_shape_replacement_fn(in_aval.shape),
      _dtype_to_ir_type(unpacked_dtype)
  )
  return tpu.unpack_elementwise(
      out_type, x, source_type=_dtype_to_ir_type(packed_dtype), index=index)

