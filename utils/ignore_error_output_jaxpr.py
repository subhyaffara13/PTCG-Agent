
def ignore_error_output_jaxpr(jaxpr, num_error_vals: int):
  """Constructs a checked jaxpr which does not output its error value."""
  consts = jaxpr.consts
  jaxpr = jaxpr.jaxpr
  new_jaxpr = jaxpr.replace(outvars=jaxpr.outvars[num_error_vals:])
  return core.ClosedJaxpr(new_jaxpr, consts)

