
def _platform_index_lowering(
    ctx: mlir.LoweringRuleContext,
    *,
    platforms: BranchesPlatforms,
):
  for i, ps in enumerate(platforms):
    # note - slightly odd structure here, as platforms is a seq[seq[str]]
    if ps is None or "mosaic" in ps:
      return ir_constant(i)

  raise NotImplementedError(
      "No mosaic or default platform indexing rule found."
  )


def _platform_index_lowering(ctx: mlir.LoweringRuleContext,
                             *,
                             platforms: BranchesPlatforms):
  def lower_constant(ctx: mlir.LoweringRuleContext, *,
                     i: int) -> Sequence[ir.Value]:
    return [mlir.ir_constant(np.int32(i))]

  platform_rules: dict[str, mlir.LoweringRule] = {}
  default_rule = None
  for i, ps in enumerate(platforms):
    rule = partial(lower_constant, i=i)
    if ps is None:
      default_rule = rule
    else:
      for p in ps:
        platform_rules[p] = rule

  return mlir.lower_per_platform(
    ctx,
    f"platform_index(platforms={platforms})",
    platform_rules, default_rule, effects.no_effects)

