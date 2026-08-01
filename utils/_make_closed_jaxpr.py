
def _make_closed_jaxpr(
    traceable,
    in_avals: Sequence[core.AbstractValue],
    debug_info: core.DebugInfo,
):
  closed_jaxpr, _ = pe.trace_to_jaxpr(
      traceable, FlatTree.flatten_args(*in_avals), debug_info
  )
  return closed_jaxpr

