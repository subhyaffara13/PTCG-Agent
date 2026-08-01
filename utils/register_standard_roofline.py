
def register_standard_roofline(prim: core.Primitive):
  def standard_rule(ctx: RooflineRuleContext, *args, **kwargs):
    return RooflineResult.zeros()

  _rooflines[prim] = standard_rule

