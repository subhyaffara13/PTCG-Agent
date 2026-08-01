
def get_available_memory(
    in_tree: tuple[jax.Array, ...], scaling_factor: float
) -> int:
  """Returns estimated available memory for broadcasting (in bytes).

  After computing the available memory, we scale it by a factor of 0.75 to
  account for the fact that the actual memory usage could be different than the
  estimated memory usage. This will help us to avoid OOM errors for edge cases.

  Args:
    in_tree: pytree that occupies the memory.
    scaling_factor: indicates the frunction of the estimated available memory to
      be used when broadcustind data.
  """
  if scaling_factor > 1:
    raise ValueError('scaling_factorshould be less than 1.')
  total_device_memory = get_device_memory()
  used_device_memory = tree_memory_per_device(in_tree)
  available_memory = total_device_memory - used_device_memory
  return int(available_memory * scaling_factor / MEMORY_FACTOR)

