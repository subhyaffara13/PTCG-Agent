
def _custom_abstract_eval(*args, jaxpr, **unused_kwargs):
  del unused_kwargs
  del args
  return jaxpr.out_avals

