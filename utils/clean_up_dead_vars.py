
def clean_up_dead_vars(eqn: JaxprEqn, env: dict[Var, Any],
                       last_used: dict[Var, JaxprEqn | None]):
  """Remove all eqn.invars from env if eqn is the last time they were used."""
  for v in {v for v in eqn.invars if not isinstance(v, Literal)}:
    if last_used[v] is eqn:
      # Delete ref to variable when it is no longer needed by next equations.
      del env[v]

