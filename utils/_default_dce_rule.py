
def _default_dce_rule(
    used_outs: list[bool], eqn: JaxprEqn
  ) -> tuple[list[bool], JaxprEqn | None]:
  if not any(used_outs) and not has_effects(eqn):
    return [False] * len(eqn.invars), None
  return [True] * len(eqn.invars), eqn

