
def _pack_elementwise_lowering_rule(
    ctx: LoweringRuleContext, *xs, packed_dtype
):
  in_aval = ctx.avals_in[0]
  out_aval = ctx.avals_out[0]
  packed_ir_type = _dtype_to_ir_type(packed_dtype)
  out_type = ir.VectorType.get(
      ctx.lowering_context.dynamic_shape_replacement_fn(in_aval.shape),
      _dtype_to_ir_type(out_aval.dtype))
  return tpu.pack_elementwise(out_type, xs, target_type=packed_ir_type)

