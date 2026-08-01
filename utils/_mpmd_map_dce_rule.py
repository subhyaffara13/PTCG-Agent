
def _mpmd_map_dce_rule(
    used_outs: list[bool], eqn: pe.JaxprEqn
) -> tuple[list[bool], pe.JaxprEqn | None]:
  return [True] * len(eqn.invars), eqn

