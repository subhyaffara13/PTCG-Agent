
def _handle_out_of_bounds_read(
    ret: np.ndarray | None,
    full_read_shape: tuple[int, ...],
    shape: Sequence[int],
    dtype: np.dtype,
    allocation_key: HostAllocationKey,
    read_range: tuple[int | slice, ...],
    shared_memory: memory.GPUSharedMemory,
    source_info,
    input_name: str | None,
    block_indices: tuple[int, ...] | None,
    grid_loop_idx: tuple[int, ...] | None,
) -> np.ndarray:
  """Handles out-of-bounds read based on shared_memory configuration."""
  if shared_memory.out_of_bounds_reads == "raise":
    if source_info is None:
      ctx = contextlib.nullcontext()
    else:
      ctx = source_info_util.user_context(
          traceback=source_info.traceback, name_stack=source_info.name_stack
      )
    with ctx:
      if input_name is None:
        raise IndexError(
            f"Out-of-bounds read of {allocation_key}:"
            f" reading [{read_range}] but buffer has shape {shape}."
        )
      else:
        # Different error message when we are reading a block of an input,
        # to copy it to a buffer before invoking the kernel body.
        raise IndexError(
            f"Out-of-bounds block index {block_indices} for {allocation_key},"
            f' input "{input_name}" in iteration {grid_loop_idx}:'
            f" reading [{read_range}] but input has shape {shape}."
        )
  # out_of_bounds_reads == "uninitialized"
  uninit_array = np.full(
      full_read_shape,
      interpret_utils.get_uninitialized_value(
          dtype, shared_memory.uninitialized_memory
      ),
      dtype=dtype,
  )
  if ret is None:
    return uninit_array
  else:
    uninit_array[tuple(slice(s) for s in ret.shape)] = ret
    return uninit_array

