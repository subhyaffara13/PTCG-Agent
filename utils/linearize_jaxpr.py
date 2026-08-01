
def linearize_jaxpr(
    jaxpr: core.ClosedJaxpr,
    nonzeros: Sequence[bool],
    instantiate: bool | Sequence[bool] = False,
    allow_fwds: bool | Sequence[bool] = True,
    *,
    is_vjp: bool,
) -> tuple[core.ClosedJaxpr, int, Sequence[bool], Sequence[int | None], core.ClosedJaxpr]:
  if type(allow_fwds) is bool:
    allow_fwds = (allow_fwds,) * (len(jaxpr.consts) + len(jaxpr.jaxpr.invars))
  assert len(allow_fwds) == (len(jaxpr.consts) + len(jaxpr.jaxpr.invars))
  if type(instantiate) is bool:
    instantiate = (instantiate,) * len(jaxpr.jaxpr.outvars)
  assert len(instantiate) == len(jaxpr.jaxpr.outvars)
  return _linearize_jaxpr(jaxpr, tuple(nonzeros), tuple(instantiate),
                          tuple(allow_fwds), is_vjp)

