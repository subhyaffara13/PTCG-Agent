
def subjaxprs(jaxpr: Jaxpr) -> Iterator[Jaxpr]:
  """Generator for all subjaxprs found in the params of jaxpr.eqns.
  Does not descend recursively into the found subjaxprs.
  """
  for eqn in jaxpr.eqns:
    yield from jaxprs_in_params(eqn.params)

