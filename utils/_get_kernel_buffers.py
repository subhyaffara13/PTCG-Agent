from typing import Any

def _get_kernel_buffers(
    token,
    device_id: int,
    num_threads: int,
    grid_mapping: pallas_core.GridMapping,
    invars: Sequence[Any],
    arg_transforms: tuple[tuple[state_types.Transform, ...], ...],
    input_buffer_keys: Sequence[jax.Array],
    output_buffer_keys: Sequence[jax.Array],
    interpret_params: InterpretGPUParams,
) -> tuple[jax.Array, list[jax.Array]]:
  """Collects buffers to be passed to the kernel from `pallas_call` input/output buffers."""
  # TODO(nrink): This code is a simplified version to the corresponding TPU
  # interpreter code. Eventually, we should merge the two.
  if not arg_transforms:
    arg_transforms = ((),) * len(invars)
  kernel_buffer_keys = []
  for i, (var, transforms) in enumerate(safe_zip(invars, arg_transforms)):
    output_idx = i - grid_mapping.num_inputs
    is_input = i < grid_mapping.num_inputs
    is_output = (output_idx >= 0) and (output_idx < grid_mapping.num_outputs)
    aval = var.aval
    # TODO(nrink): Support allocation of semaphores.
    if gpu_callbacks.is_gmem_memory_space(aval.memory_space):
      # Use the already-allocated GMEM input or output buffer.
      #
      # TODO(jburnim): For kernel args in GMEM, check that block shape equals
      # the shape of the corresponding `pallas_call` input, and that the
      # index_map is trivial.
      assert is_input ^ is_output
      if is_input:
        kernel_buffer_keys.append(input_buffer_keys[i])
      if is_output:
        kernel_buffer_keys.append(output_buffer_keys[output_idx])
    else:
      token, req = gpu_callbacks.call_make_allocation_request_array(
          token=token,
          device_id=jnp.int32(device_id),
          memory_space_id=gpu_callbacks.get_memory_space_idx(aval.memory_space),
          initial_ref_count=num_threads,
      )
      if transforms:
        # The invar/aval's shape in the jaxpr may be the tiled shape, after
        # tiling and/or swizzling transforms have been applied.  The
        # elements of `transforms` -- to undo the swizzling and/or tiling --
        # are applied any time the variable is used in the jaxpr.
        #
        # We want to allocate a buffer with the logical shape, instead of
        # the tiled shape, so we undo the swizzing and/or tiling here to get
        # the logical shape.
        aval = jaxpr_interpret.apply_unswizzle_and_untile(transforms, aval)
      init_val = jaxpr_interpret.get_uninitialized_array(
          aval.shape,
          aval.dtype,
          aval.memory_space,
          interpret_params.uninitialized_memory
      )
      token, key = gpu_callbacks.call_allocate_buffer_for_all_threads(
          token, jnp.int32(device_id), None, req, init_val
      )
      kernel_buffer_keys.append(key)

  return token, kernel_buffer_keys

