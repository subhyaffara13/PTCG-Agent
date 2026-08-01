
def partial_eval_jaxpr_nounits_fwd(
    jaxpr: ClosedJaxpr, unknowns: Sequence[bool],
    instantiate: bool | Sequence[bool],
    fwd: bool | Sequence[bool] = True,
) -> tuple[ClosedJaxpr, ClosedJaxpr, list[bool], list[AbstractValue], list[int | None]]:
  instantiate = tuple(instantiate) if isinstance(instantiate, list) else instantiate
  fwd = tuple(fwd) if isinstance(fwd, list) else fwd
  return _partial_eval_jaxpr_nounits(jaxpr, tuple(unknowns), instantiate, fwd)

