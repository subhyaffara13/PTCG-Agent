
def get_thread_id_for_collective_allocation_key(
    thread_id: int,
    axes_dims: tuple[int, ...],
    is_last_thread_axis_collective: bool,
) -> int:
  """Returns the thread ID to use for the allocation key in a collective allocation.

  Only the last thread coordinate (corresponding to the threads in a block) can
  be collective; whether this is the case is determined by
  `is_last_thread_axis_collective`.

  Args:
    thread_id: A 'flat' thread ID.
    axes_dims: The dimensions of the cluster axes and block (row-major order,
      where the last/minor-most dimension is the block dimension).
    is_last_thread_axis_collective: A boolean indicating whether the last thread
      axis (correspodning to the threads in a block) is collective.

  Returns:
    The thread ID to use for the allocation key in a collective allocation.
  """
  if is_last_thread_axis_collective:
    return thread_id // axes_dims[-1]
  else:
    return thread_id

