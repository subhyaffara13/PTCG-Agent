from typing import Any

def resolve_physical_types(jaxpr: jax_core.Jaxpr, consts: Sequence[Any]):
  kernel_avals = jax_core.ClosedJaxpr(jaxpr, consts).in_avals
  kernel_avals = tuple(map(_logical_aval_to_interpret_mode_aval,
                             kernel_avals))
  interp_fun = partial(
      eval_jaxpr_recursive, jaxpr, consts,
      recurse_hop_rule=resolve_physical_types)
  wrapped = lu.wrap_init(interp_fun, debug_info=jaxpr.debug_info)
  new_jaxpr, _, new_consts = pe.trace_to_jaxpr_dynamic(
      wrapped, kernel_avals)
  return new_jaxpr, new_consts

