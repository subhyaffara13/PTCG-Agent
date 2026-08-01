
def _add_constraint_system_derivation_rule(op: type[ir.OpView]):
  def wrapper(rule: ConstraintSystemDerivationRule):
    if op is not None:
      assert hasattr(op, "OPERATION_NAME")
      _constraint_system_derivation_rules[op.OPERATION_NAME] = rule
    return rule

  return wrapper

