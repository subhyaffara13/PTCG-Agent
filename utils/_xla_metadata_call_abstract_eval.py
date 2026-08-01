
def _xla_metadata_call_abstract_eval(*in_avals, jaxpr, **meta):
  return jaxpr.out_avals

