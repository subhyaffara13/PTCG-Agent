from typing import Any

def _jet_jaxpr(
    jaxpr: core.ClosedJaxpr, order: int, primals_and_series_avals, in_tree_def
) -> tuple[core.ClosedJaxpr, Any]:
  f = lu.wrap_init(core.jaxpr_as_fun(jaxpr),
                   debug_info=jaxpr.jaxpr.debug_info.with_unknown_names())
  f_jet, out_tree_def = traceable(jet_fun(jet_subtrace(f), order), in_tree_def)
  jaxpr_jet, _, consts = pe.trace_to_jaxpr_dynamic(
      f_jet, primals_and_series_avals)
  return core.ClosedJaxpr(jaxpr_jet, consts), out_tree_def

