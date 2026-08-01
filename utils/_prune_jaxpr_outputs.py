
def _prune_jaxpr_outputs(jaxpr: Jaxpr, used_outputs: tuple[bool, ...]) -> Jaxpr:
  outvars = [v for v, b in zip(jaxpr.outvars, used_outputs) if b]
  dbg = core.DebugInfo(
      jaxpr.debug_info.traced_for, jaxpr.debug_info.func_src_info,
      jaxpr.debug_info.arg_names,
      jaxpr.debug_info.filter_result_paths(used_outputs))
  new_jaxpr = jaxpr.replace(outvars=outvars, debug_info=dbg)
  config.enable_checks.value and core.check_jaxpr(new_jaxpr)
  return new_jaxpr

