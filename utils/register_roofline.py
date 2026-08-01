
def register_roofline(prim: core.Primitive):
  def register(rule: _RooflineRule):
    _rooflines[prim] = rule
    return rule

  return register

