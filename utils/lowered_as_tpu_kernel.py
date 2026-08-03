from typing import Any, Callable

def lowered_as_tpu_kernel(
    lowered_module: ir.Module,
    out_type: Any,
    *,
    collective_id: int | None = None,
    cost_estimate: CostEstimate | None = None,
    needs_hlo_passes: bool = False,
    needs_layout_passes: bool = False,
    has_communication: bool = False,
    has_side_effects: bool | TpuSideEffectType = False,
    has_custom_barrier: bool = False,
    kernel_name: str | None = None,
    vmem_limit_bytes: int | None = None,
    flags: dict[str, bool | int | float] | None = None,
    allow_input_fusion: Sequence[bool] | None = None,
    input_output_aliases: tuple[tuple[int, int], ...] = (),
    serialization_format: int | None = None,
    internal_scratch_in_bytes: int | None = None,
    disable_bounds_checks: bool = False,
    disable_semaphore_checks: bool = False,
    metadata: Any | None = None,
    allow_collective_id_without_custom_barrier: bool = False,
) -> Callable[..., Any]:
  device_type = _get_device_type(lowered_module)
  lowered_module_asm = cast(
      bytes,
      lowered_module.operation.get_asm(binary=True, enable_debug_info=True),
  )
  if isinstance(has_side_effects, bool):
    has_side_effects = (
        TpuSideEffectType.PURE
        if not has_side_effects
        else TpuSideEffectType.DATAFLOW_SIDE_EFFECTING
    )
  config = _lowered_to_custom_call_config(
      lowered_module_asm,
      lowered_module_asm_version=None,
      vmem_limit_bytes=vmem_limit_bytes,
      cost_estimate=cost_estimate,
      flags=flags,
      allow_input_fusion=allow_input_fusion,
      internal_scratch_in_bytes=internal_scratch_in_bytes,
      collective_id=collective_id,
      device_type=device_type,
      serialization_format=serialization_format,
      has_custom_barrier=has_custom_barrier,
      has_communication=has_communication,
      needs_hlo_passes=needs_hlo_passes,
      needs_layout_passes=needs_layout_passes,
      disable_bounds_checks=disable_bounds_checks,
      disable_semaphore_checks=disable_semaphore_checks,
      allow_collective_id_without_custom_barrier=allow_collective_id_without_custom_barrier,
  )
  return _as_jax_callable(
      config,
      has_side_effects,
      out_type,
      kernel_name=kernel_name,
      input_output_aliases=input_output_aliases,
      metadata=metadata,
  )

