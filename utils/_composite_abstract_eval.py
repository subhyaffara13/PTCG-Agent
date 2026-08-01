
def _composite_abstract_eval(*args, jaxpr, **_):
  del args
  return jaxpr.out_avals

