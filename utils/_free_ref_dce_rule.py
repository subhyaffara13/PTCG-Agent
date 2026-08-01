
def _free_ref_dce_rule(
    used_outs: list[bool], eqn: JaxprEqn
) -> tuple[list[bool], JaxprEqn | None]:
  # Never gonna DCE free_ref.
  del used_outs
  return [True] * len(eqn.invars), eqn

