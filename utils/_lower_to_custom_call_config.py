
def _lower_to_custom_call_config(
    module: ir.Module,
    *,
    vmem_limit_bytes: int | None,
    cost_estimate: CostEstimate | None,
    flags: dict[str, bool | int | float] | None,
    allow_input_fusion: Sequence[bool] | None,
    internal_scratch_in_bytes: int | None,
    collective_id: int | None,
    serialization_format: int | None,
    output_memory_spaces: tuple[MemorySpace | None, ...] | None = None,
    ir_version: int | None = None,
    disable_bounds_checks: bool = False,
    disable_semaphore_checks: bool = False,
    input_memory_spaces: tuple[MemorySpace | None, ...] | None = None,
    skip_device_barrier: bool = False,
    allow_collective_id_without_custom_barrier: bool = False,
    shape_invariant_numerics: bool = False,
    needs_layout_passes: bool | None = None,
    tiling: Tiling | None = None,
) -> CustomCallBackendConfig:
  device_type = _get_device_type(module)
  needs_hlo_passes = config.jax_mosaic_allow_hlo.value
  # TC kernels always require layout passes.
  needs_layout_passes = needs_layout_passes or not device_type
  lowered_module_asm, (
      has_communication,
      has_custom_barrier,
  ) = _lower_mosaic_module_to_asm(
      module,
      ir_version=ir_version,
  )
  active_core_count = _get_active_core_count(module)
  return _lowered_to_custom_call_config(
      lowered_module_asm,
      lowered_module_asm_version=ir_version,
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
      output_memory_spaces=output_memory_spaces,
      disable_bounds_checks=disable_bounds_checks,
      disable_semaphore_checks=disable_semaphore_checks,
      active_core_count=active_core_count,
      input_memory_spaces=input_memory_spaces,
      skip_device_barrier=skip_device_barrier,
      allow_collective_id_without_custom_barrier=allow_collective_id_without_custom_barrier,
      shape_invariant_numerics=shape_invariant_numerics,
      tiling=tiling,
  )

