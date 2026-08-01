
def _get_lowering_rules(
    ctx: ModuleContext, primitive: core.Primitive,
    eqn_ctx: core.JaxprEqnContext | None
) -> tuple[dict[str, LoweringRule], LoweringRule | None, bool]:
  override_rule = _get_override_lowering_rule(ctx, primitive)
  # See lower_per_platform for meaning of `platform_rules` and `default_rule`
  platform_rules: dict[str, LoweringRule] = {}
  default_rule: LoweringRule | None = None
  inline = True  # Should calls to this lowering rule be inlined?

  if override_rule is not None:
    default_rule = override_rule
    assert not isinstance(default_rule, LoweringRuleEntry)
  else:
    # First the platform-specific rules
    for p in _platforms_for_eqn_ctx(eqn_ctx) or ctx.platforms:
      if primitive in _platform_specific_lowerings[p]:
        r = _platform_specific_lowerings[p][primitive]
        platform_rules[p] = r.rule
        inline = inline and r.inline
    # Now the default rule
    if primitive in _lowerings:
      r = _lowerings[primitive]
      default_rule = r.rule
      assert not isinstance(default_rule, LoweringRuleEntry)
      inline = inline and r.inline

  return platform_rules, default_rule, inline

