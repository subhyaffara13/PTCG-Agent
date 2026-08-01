
def rearrange_binders(jaxpr: core.ClosedJaxpr, primals_in, tangents_in, primals_out, tangents_out):
  new_invars = _perm(primals_in, tangents_in, jaxpr.jaxpr.invars)
  new_outvars = _perm(primals_out, tangents_out, jaxpr.jaxpr.outvars)
  if jaxpr.jaxpr.debug_info.arg_names is None:
    new_arg_names = None
  else:
    new_arg_names = tuple(_perm(primals_in, tangents_in,
                                jaxpr.jaxpr.debug_info.arg_names))
  if jaxpr.jaxpr.debug_info.result_paths is None:
    new_result_paths = None
  else:
    new_result_paths = tuple(_perm(primals_out, tangents_out,
                                   jaxpr.jaxpr.debug_info.result_paths))
  new_debug_info = jaxpr.jaxpr.debug_info._replace(
      arg_names=new_arg_names, result_paths=new_result_paths)
  new_jaxpr = jaxpr.jaxpr.replace(
      invars=new_invars, outvars=new_outvars, debug_info=new_debug_info)
  return core.ClosedJaxpr(new_jaxpr, jaxpr.consts)

