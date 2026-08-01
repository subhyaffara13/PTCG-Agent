
def _logistic_lowering_rule(ctx: LoweringRuleContext, x, accuracy=None):
  if accuracy is not None:
    raise NotImplementedError("Not implemented: accuracy")
  neg_x = arith.negf(x)
  exp_neg_x = mlir_math.exp(neg_x)
  aval_out = ctx.avals_out[0]
  out_type = ctx.aval_to_ir_type(aval_out)
  if not aval_out.shape:
    one = ir_constant(1.0, mlir_type=out_type)
  else:
    one = vector.broadcast(
        out_type, ir_constant(1.0, _dtype_to_ir_type(aval_out.dtype))
    )
  denom = arith.addf(one, exp_neg_x)
  return arith.divf(one, denom)

