
def register_discharge_rule(prim: core.Primitive):
  def register(f: DischargeRule):
    _discharge_rules[prim] = f
    return f

  return register

