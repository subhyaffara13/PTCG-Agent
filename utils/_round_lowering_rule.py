
def _round_lowering_rule(ctx: LoweringRuleContext, x, *, rounding_method):
  if rounding_method == 0:
    return mlir_math.round(x)
  elif rounding_method == 1:
    return mlir_math.roundeven(x)
  else:
    raise NotImplementedError(f"Unsupported rounding method: {rounding_method}")


def _round_lowering_rule(ctx: LoweringRuleContext, x, rounding_method):
  [x_aval] = ctx.avals_in
  x = _ensure_fa(x, x_aval.dtype)
  match rounding_method:
    case lax.RoundingMethod.AWAY_FROM_ZERO:
      return x.round()
    case lax.RoundingMethod.TO_NEAREST_EVEN:
      return x.round_even()
    case _:
      assert_never(rounding_method)

