
def _cached_trace_to_jaxpr(f, in_type):
  jaxpr, out_type, consts = trace_to_jaxpr_dynamic(lu.annotate(f, in_type), in_type)
  return jaxpr, out_type, consts

