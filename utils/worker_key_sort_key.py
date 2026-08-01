
def worker_key_sort_key(worker_key: tuple[int, ...]) -> tuple[int, ...]:
  """Sorts `(task, slice)` Pathways worker keys in slice-major order.

  Args:
    worker_key: The input worker key.

  Returns:
    The worker key reordered for sorting.
  """
  if len(worker_key) == 2:
    task_index, slice_index = worker_key
    return (slice_index, task_index)
  return worker_key

