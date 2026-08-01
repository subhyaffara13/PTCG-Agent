
def _lowered_to_custom_call_config(
    lowered_module_asm: bytes,
    *,
    lowered_module_asm_version: int | None,
    vmem_limit_bytes: int | None,
    cost_estimate: CostEstimate | None,
    flags: dict[str, bool | int | float] | None,
    allow_input_fusion: Sequence[bool] | None,
    internal_scratch_in_bytes: int | None,
    collective_id: int | None,
    serialization_format: int | None,
    has_custom_barrier: bool,
    has_communication: bool,
    needs_hlo_passes: bool,
    needs_layout_passes: bool,
    device_type: str | None,
    output_memory_spaces: tuple[MemorySpace | None, ...] | None = None,
    disable_bounds_checks: bool = False,
    disable_semaphore_checks: bool = False,
    active_core_count: int | None = None,
    input_memory_spaces: tuple[MemorySpace | None, ...] | None = None,
    skip_device_barrier: bool = False,
    allow_collective_id_without_custom_barrier: bool = False,
    shape_invariant_numerics: bool = False,
    tiling: Tiling | None = None,
):
  if has_custom_barrier:
    if collective_id is None:
      raise ValueError(
          "collective_id has to be specified when using a custom barrier"
      )
  elif collective_id is not None and not allow_collective_id_without_custom_barrier:
    raise ValueError(
        "collective_id has to be unspecified or None when not using a custom"
        " barrier"
    )
  if vmem_limit_bytes is not None and not isinstance(vmem_limit_bytes, int):
    raise ValueError(
        "vmem_limit_bytes must be an int: provided with a"
        f" {type(vmem_limit_bytes)}."
    )
  if tiling is not None and  device_type != "sparsecore":
    raise ValueError(
        "explicit tiling is only supported for SparseCore kernels."
    )
  return CustomCallBackendConfig(
      lowered_module_asm,
      lowered_module_asm_version,
      has_communication,
      collective_id,
      device_type,
      cost_estimate,
      needs_hlo_passes,
      needs_layout_passes,
      vmem_limit_bytes,
      flags,
      allow_input_fusion,
      serialization_format,
      internal_scratch_in_bytes,
      output_memory_spaces,
      disable_bounds_checks,
      disable_semaphore_checks,
      active_core_count=active_core_count,
      input_memory_spaces=input_memory_spaces,
      skip_device_barrier=skip_device_barrier,
      shape_invariant_numerics=shape_invariant_numerics,
      tiling=tiling,
  )

