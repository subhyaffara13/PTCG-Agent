
def _uncached_lowering(
    primitive: core.Primitive,
    eqn_ctx: core.JaxprEqnContext,
    effects: effects_lib.Effects,
    platform_rules: dict[str, LoweringRule],
    default_rule: LoweringRule | None,
    ctx: LoweringRuleContext,
    *args,
    **params,
):

  assert not isinstance(default_rule, LoweringRuleEntry)
  assert not any(isinstance(r, LoweringRuleEntry) for r in platform_rules.values())
  ans = lower_per_platform(ctx, str(primitive), platform_rules, default_rule,
                           effects, *args, **params)
  try:
    rets = tuple(ans)
  except TypeError as e:
    raise ValueError("Output of translation rule must be iterable: "
                      f"{primitive}, got output {ans}") from e

  ordered_effects = list(effects_lib.ordered_effects.filter_in(effects))
  if ordered_effects:
    # If there were ordered effects in the primitive, there should be output
    # tokens we need for subsequent ordered effects.
    tokens_out = ctx.tokens_out
    if tokens_out is None:
      raise ValueError(
          f'Lowering rule for `{primitive}` needs to set `tokens_out` '
          f'because it has effects: {effects}.')
    if tokens_out.effects() != ctx.tokens_in.effects():
      raise ValueError(
          f"Lowering rule for `{primitive}` returns incorrect set of output"
          f" tokens. Expected: {tuple(ctx.tokens_in.effects())} vs. Actual:"
          f" {tuple(tokens_out.effects())}"
      )
  return rets

