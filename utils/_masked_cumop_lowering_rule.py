
def _masked_cumop_lowering_rule(ctx: sc_lowering.LoweringRuleContext, x, mask,
                                *, reduction_kind: str):
  sign_bit_vec = None
  # tpu.scan comparisons assume unsigned int predicates, so we compare
  # with the sign bit flipped.
  if ctx.avals_in[0].dtype == jnp.dtype(jnp.int32) and reduction_kind in ("max", "min"):
    i32 = ir.IntegerType.get_signless(32)
    sign_bit_vec = vector.broadcast(
        x.type, arith.constant(i32, ir.IntegerAttr.get(i32, 0x80000000)))
    x = arith.xori(x, sign_bit_vec)
  result = tpu.scan(
      x.type, x, ir.Attribute.parse(f"#tpu.reduction_kind<{reduction_kind}>"),
      mask=mask)
  if sign_bit_vec is not None:  # Flip the sign bit back
    return arith.xori(result, sign_bit_vec)
  return result

