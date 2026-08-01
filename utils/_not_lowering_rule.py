
def _not_lowering_rule(ctx: LoweringRuleContext, x):
  # The primitive not_p is lowered to
  # https://github.com/openxla/stablehlo/blob/main/docs/spec.md#not
  # which is arithmetic for integers and logical for booleans.
  # Lowering to:
  # xor x, -1
  # covers both cases.
  out_aval = ctx.avals_out[0]
  out_scalar_type = _dtype_to_ir_type(out_aval.dtype)
  if not out_aval.shape:
    # Create a scalar constant.
    minus_one = ir_constant(-1, out_scalar_type)
  else:
    # Create a vector constant.
    out_type = ctx.aval_to_ir_type(out_aval)
    scalar_minus_one = ir.IntegerAttr.get(out_scalar_type, -1)
    minus_one = arith.constant(
        out_type, ir.DenseElementsAttr.get_splat(out_type, scalar_minus_one)
    )
  return arith.xori(x, minus_one)


def _not_lowering_rule(ctx: LoweringRuleContext, x):
  [x_aval] = ctx.avals_in
  return arith_dialect.xori(x, _full(x.type, ~x_aval.dtype.type(0)))

