
def _allocate_buffers_for_outputs(
    token,
    device_id: int,
    num_threads: int,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: pallas_core.GridMapping,
    input_buffer_keys: Sequence[jax.Array],
    input_vals: Sequence[jax.Array],
    interpret_params: InterpretGPUParams,
) -> tuple[jax.Array, list[AllocationKeyAndValue]]:
  """Allocates `GMEM` buffers for `pallas_call` outputs, respecting aliased inputs."""
  # TODO(nrink): This code is a simplified version to the corresponding TPU
  # interpreter code. Eventually, we should merge the two.
  assert len(input_buffer_keys) == len(input_vals)

  oi_alias_map = {v: k for k, v in input_output_aliases}
  output_buffer_keys_and_values = []

  block_shapes = [
      pallas_core._get_block_shape(bm.block_shape)
      for bm in grid_mapping.block_mappings
  ]
  num_inputs = grid_mapping.num_inputs

  num_outputs = grid_mapping.num_outputs
  output_block_shapes = block_shapes[num_inputs : num_inputs + num_outputs]
  for output_idx, bm in enumerate(grid_mapping.block_mappings_output):
    if output_idx in oi_alias_map:
      aliased_input_idx = oi_alias_map[output_idx]
      # Reuse the `GMEM` buffer for the aliased `pallas_call`/`core_map` input.
      output_buffer_keys_and_values.append(
          AllocationKeyAndValue(
              key=input_buffer_keys[aliased_input_idx],
              value=input_vals[aliased_input_idx],
          )
      )
    else:
      out_val = interpret_utils.get_uninitialized_array(
          bm.array_aval.shape, bm.array_aval.dtype,
          interpret_params.uninitialized_memory)
      padded_val = interpret_utils.pad_to_block_dimension(
          out_val, output_block_shapes[output_idx],
          interpret_params.uninitialized_memory)
      token, req = gpu_callbacks.call_make_allocation_request_array(
          token=token,
          device_id=jnp.int32(device_id),
          # All outputs of a `pallas_call`/`core_map` that are arrays (i.e. that
          # are not sempahores, barriers etc.) are placed in `GMEM`. Results
          # from executing the kernel (or slices thereof) may need to be copied
          # from `SMEM` into the `GMEM` output buffers that are allocated here.
          memory_space_id=gpu_callbacks.get_memory_space_idx(
              mosaic_gpu_core.MemorySpace.GMEM
          ),
          initial_ref_count=num_threads,
      )
      token, key = gpu_callbacks.call_allocate_buffer_for_all_threads(
          token, jnp.int32(device_id), None, req, padded_val
      )
      output_buffer_keys_and_values.append(
          AllocationKeyAndValue(key=key, value=out_val)
      )

  return token, output_buffer_keys_and_values

