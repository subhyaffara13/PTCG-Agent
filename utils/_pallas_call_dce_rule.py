
def _pallas_call_dce_rule(
    used_outs: list[bool], eqn: pe.JaxprEqn
) -> tuple[list[bool], pe.JaxprEqn | None]:
  del used_outs
  return [True] * len(eqn.invars), eqn

