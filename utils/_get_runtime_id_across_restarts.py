from typing import List, Optional

def _get_runtime_id_across_restarts(
    previous_runtime_to_dist_id: Optional[List[int]],
) -> List[Optional[int]]:
  """Get runtime id changes across restarts.

  Args:
    previous_runtime_to_dist_id: mapping from runtime process index to
      distributed process index of the previous incarnation.

  Returns:
    Integer list which maps previous runtime id (index) to current runtime id
    (array element).
  Raises:
    ValueError:
  """
  current_dist_to_runtime_id = _int_list_flip_index_and_value(
      runtime_to_distributed_ids()
  )
  previous_dist_to_runtime_id = _int_list_flip_index_and_value(
      previous_runtime_to_dist_id
  )

  result = [None for _ in range(jax.process_count())]
  # Previous runtime id (index) to current runtime id (value).
  for i in range(jax.process_count()):
    result[previous_dist_to_runtime_id[i]] = current_dist_to_runtime_id[i]
  assert None not in result
  return result

