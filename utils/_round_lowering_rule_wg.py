
def _round_lowering_rule_wg(ctx: LoweringRuleContext, x, rounding_method):
  [x_aval] = ctx.avals_in
  x = _ensure_ir_value(x, x_aval.dtype)
  if not jnp.issubdtype(x_aval.dtype, jnp.floating):
    raise NotImplementedError(f"Unsupported dtype for round: {x_aval.dtype}")
  match rounding_method:
    case lax.RoundingMethod.AWAY_FROM_ZERO:
      return math_dialect.round(x)
    case lax.RoundingMethod.TO_NEAREST_EVEN:
      return math_dialect.roundeven(x)
    case _:
      assert_never(rounding_method)

