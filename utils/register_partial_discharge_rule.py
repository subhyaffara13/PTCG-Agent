
def register_partial_discharge_rule(prim: core.Primitive):
  def register(f: PartialDischargeRule):
    _partial_discharge_rules[prim] = f
  return register

