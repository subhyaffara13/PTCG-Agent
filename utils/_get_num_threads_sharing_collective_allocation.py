
def _get_num_threads_sharing_collective_allocation(
    axes_dims: tuple[int, ...],
    is_last_thread_axis_collective: bool,
) -> int:
  """Returns the number of threads that share a collective allocation."""
  if is_last_thread_axis_collective:
    return axes_dims[-1]
  else:
    return 1

