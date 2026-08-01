
def _jaxpr_forwarding(jaxpr: Jaxpr) -> list[int | None]:
  # Compute which inputs are just forwarded to outputs.
  fwds: dict[Var, Atom] = dict(zip(jaxpr.invars, jaxpr.invars))
  for eqn in jaxpr.eqns:
    if eqn.primitive in forwarding_rules:
      eqn = eqn.replace(invars=[a if type(a) is Literal else fwds.get(a, a)
                                for a in eqn.invars])
      fwd_idx, _ = forwarding_rules[eqn.primitive](eqn)
      for v_orig, idx in zip(eqn.outvars, fwd_idx):
        if idx is not None:
          fwds[v_orig] = eqn.invars[idx]
  idxs: dict[Var, int] = {v: i for i, v in enumerate(jaxpr.invars)}
  return [None if type(v) is Literal else idxs.get(fwds.get(v))  # pyrefly: ignore[bad-argument-type]
          for v in jaxpr.outvars]

