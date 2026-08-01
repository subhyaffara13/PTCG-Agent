
def _all_eqns_with_traceback(
    jaxpr: core.Jaxpr, caller_tb: xla_client.Traceback | None,
    visited: set[core.Jaxpr]
) -> Iterator[tuple[xla_client.Traceback | None, core.JaxprEqn]]:
  for eqn in jaxpr.eqns:
    tb = eqn.source_info.traceback
    if caller_tb is not None:
      tb = caller_tb if tb is None else tb + caller_tb
    yield tb, eqn

    for subjaxpr in core.jaxprs_in_params(eqn.params):
      if subjaxpr not in visited:
        visited.add(subjaxpr)
        yield from _all_eqns_with_traceback(subjaxpr, tb, visited)

