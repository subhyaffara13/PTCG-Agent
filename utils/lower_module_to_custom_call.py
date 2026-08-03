from typing import Any

def lower_module_to_custom_call(
    ctx: mlir.LoweringRuleContext,
    *in_nodes: ir.Value,
    module: ir.Module,
    out_type: Any,
    kernel_name: str,
    cost_estimate: CostEstimate | None,
    vmem_limit_bytes: int | None,
    flags: dict[str, bool | int | float] | None,
    allow_input_fusion: Sequence[bool] | None,
    input_output_aliases: tuple[tuple[int, int], ...],
    internal_scratch_in_bytes: int | None,
    collective_id: int | None,
    has_side_effects: bool | TpuSideEffectType,
    serialization_format: int | None,
    output_memory_spaces: tuple[MemorySpace | None, ...] | None,
    disable_bounds_checks: bool = False,
    disable_semaphore_checks: bool = False,
    input_memory_spaces: tuple[MemorySpace | None, ...] | None,
    metadata: Any | None = None,
    skip_device_barrier: bool = False,
    allow_collective_id_without_custom_barrier: bool = False,
    shape_invariant_numerics: bool = False,
    needs_layout_passes: bool | None = None,
    tiling: Tiling | None = None,
) -> Sequence[ir.Value]:
  if isinstance(has_side_effects, bool):
    has_side_effects = (
        TpuSideEffectType.PURE
        if not has_side_effects
        else TpuSideEffectType.SIDE_EFFECTING
    )
  config = _lower_to_custom_call_config(
      module,
      vmem_limit_bytes=vmem_limit_bytes,
      cost_estimate=cost_estimate,
      flags=flags,
      allow_input_fusion=allow_input_fusion,
      internal_scratch_in_bytes=internal_scratch_in_bytes,
      collective_id=collective_id,
      serialization_format=serialization_format,
      output_memory_spaces=output_memory_spaces,
      ir_version=get_ir_version(ctx),
      disable_bounds_checks=disable_bounds_checks,
      disable_semaphore_checks=disable_semaphore_checks,
      input_memory_spaces=input_memory_spaces,
      skip_device_barrier=skip_device_barrier,
      allow_collective_id_without_custom_barrier=allow_collective_id_without_custom_barrier,
      shape_invariant_numerics=shape_invariant_numerics,
      needs_layout_passes=needs_layout_passes,
      tiling=tiling,
  )
  return _tpu_custom_call_lowering(
      ctx,
      *in_nodes,
      config=config,
      has_side_effects=has_side_effects,
      kernel_name=kernel_name,
      out_avals=out_type,
      input_output_aliases=input_output_aliases,
      metadata=metadata,
  )

