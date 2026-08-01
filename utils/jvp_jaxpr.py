
def jvp_jaxpr(jaxpr: core.ClosedJaxpr, nonzeros: Sequence[bool],
              instantiate: bool | Sequence[bool]
              ) -> tuple[core.ClosedJaxpr, list[bool]]:
  if type(instantiate) is bool:
    instantiate = (instantiate,) * len(jaxpr.out_avals)
  return _jvp_jaxpr(jaxpr, tuple(nonzeros), tuple(instantiate))

