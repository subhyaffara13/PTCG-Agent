
def _maybe_cast_store_to_memref_type(
    ctx: LoweringRuleContext, expected_aval, val: ir.Value
) -> ir.Value:
  """Casts a boolean value back to an integer for storing in a memref."""
  if expected_aval.dtype != jnp.bool_:
    return val
  int_out_type = ctx.aval_to_ir_type(expected_aval, is_kernel_boundary=True)
  return arith.extui(int_out_type, val)

