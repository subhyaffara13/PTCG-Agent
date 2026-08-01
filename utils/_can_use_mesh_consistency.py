
def _can_use_mesh_consistency(
    previous_distributed_to_device_ids: list[list[int]],
    current_distributed_to_device_ids: list[list[int]],
    previous_device_ids: list[int],
) -> bool:
  """Returns whether mesh consistency applies.

  Args:
    previous_distributed_to_device_ids: The mapping stored in the checkpoint.
    current_distributed_to_device_ids: The runtime mapping of the environment.
    previous_device_ids: Global physical order of the past workers.

  Returns:
    True if the checkpoint's physical topology matches the runtime, else
    False.
  """
  previous_device_count = sum(
      len(device_ids) for device_ids in previous_distributed_to_device_ids
  )
  current_device_count = sum(
      len(device_ids) for device_ids in current_distributed_to_device_ids
  )
  return (
      len(previous_distributed_to_device_ids)
      == len(current_distributed_to_device_ids)
      and previous_device_count == current_device_count
      and len(previous_device_ids) == current_device_count
  )

