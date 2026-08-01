
def build_mlir_module_helper(
    closed_jaxpr: core.ClosedJaxpr, *, name: str,
    platforms: Sequence[str],
    backend: xc.Client | None,
    axis_context: AxisContext) -> ir.Module:
  """Helper to generate pmap-style XLA computations for custom partitioners."""
  unlowerable_effects = effects_lib.lowerable_effects.filter_not_in(
      closed_jaxpr.effects)
  if unlowerable_effects:
    raise ValueError(f'Cannot lower jaxpr with effects: {closed_jaxpr.effects}')
  lowering_result = lower_jaxpr_to_module(name, closed_jaxpr,
      num_const_args=0,
      in_avals=closed_jaxpr.in_avals,
      backend=backend, ordered_effects=[],
      donated_args=[False] * len(closed_jaxpr.jaxpr.invars),
      axis_context=axis_context, platforms=platforms,
      lowering_parameters=LoweringParameters(hoist_constants_as_args=False))
  return lowering_result.module

