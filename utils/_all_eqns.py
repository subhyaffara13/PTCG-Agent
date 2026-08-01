
def _all_eqns(
    jaxpr: core.Jaxpr, visited: set[core.Jaxpr] | None,
) -> Iterator[tuple[core.Jaxpr, core.JaxprEqn]]:
  for eqn in jaxpr.eqns:
    yield (jaxpr, eqn)
  for subjaxpr in core.subjaxprs(jaxpr):
    if visited is None:
      yield from _all_eqns(subjaxpr, visited)
    elif subjaxpr not in visited:
      visited.add(subjaxpr)
      yield from _all_eqns(subjaxpr, visited)

