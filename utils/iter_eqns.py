
def iter_eqns(jaxpr):
  # TODO(necula): why doesn't this search in params?
  yield from jaxpr.eqns
  for subjaxpr in core.subjaxprs(jaxpr):
    yield from iter_eqns(subjaxpr)

