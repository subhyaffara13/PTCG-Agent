from typing import Any

def kernel_to_hlo_jaxpr(
    jaxpr: jax_core.Jaxpr, consts: Sequence[Any], grid_mapping: GridMapping
) -> tuple[jax_core.Jaxpr, Sequence[Any], Sequence[Any]]:
  """Converts a Pallas kernel jaxpr to a valid HLO jaxpr."""
  with grid_mapping.trace_env():
    # TODO(justinfu): Evaluate backend-specific primitives in a new pass.
    phys_jaxpr, phys_consts = resolve_physical_types(jaxpr, consts)
    # For now, we assume that physical types are 1:1 with logical types
    # so that the indexing of scratch vars is unchanged.
    assert len(phys_jaxpr.invars) == len(jaxpr.invars)
    scratch_invars = phys_jaxpr.invars[grid_mapping.slice_scratch_ops]
    scratch_avals = [v.aval for v in scratch_invars]
    discharged_closed_jaxpr = state_discharge.discharge_state(
        jax_core.ClosedJaxpr(phys_jaxpr, phys_consts))
  return discharged_closed_jaxpr.jaxpr, discharged_closed_jaxpr.consts, scratch_avals

