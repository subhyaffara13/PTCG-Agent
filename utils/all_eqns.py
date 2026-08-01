
def all_eqns(
    jaxpr: core.Jaxpr, revisit_inner_jaxprs: bool = True
) -> Iterator[tuple[core.Jaxpr, core.JaxprEqn]]:
  yield from _all_eqns(jaxpr, None if revisit_inner_jaxprs else set())

