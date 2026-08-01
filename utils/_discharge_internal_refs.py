
def _discharge_internal_refs(jaxpr: core.ClosedJaxpr) -> core.ClosedJaxpr:
  # TODO(slebedev): Inline this function.
  from jax._src.state.discharge import discharge_state  # pyrefly: ignore[missing-import]
  discharged_jaxpr = discharge_state(jaxpr)
  return discharged_jaxpr.replace(
      jaxpr=discharged_jaxpr.jaxpr.replace(debug_info=jaxpr.jaxpr.debug_info)
  )

