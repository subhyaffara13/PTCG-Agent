
def _dce_consts(jaxpr, consts):
  jaxpr, used_consts, _ = pe.dce_jaxpr_consts(
      jaxpr, [True] * len(jaxpr.outvars),
      [False] * len(jaxpr.constvars) + [True] * len(jaxpr.invars))
  return jaxpr, [c for c, used in zip(consts, used_consts) if used]

