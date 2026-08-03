import logging

def _initialize_jax_from_mtc(
    local_checkpoint_directory: epath.Path,
    jax_initialization_timeout_seconds: int = 900,
) -> str:
  """Initialize jax with jax_init_info."""
  local_checkpoint_directory = epath.Path(local_checkpoint_directory)
  process_id, coordinator_address = _retrieve_jax_init_info(
      local_checkpoint_directory
  )
  if not process_id or not coordinator_address:
    raise ValueError(
        'Data is missing from the JAX init info file: Current values:'
        f' process_id: {process_id}, coordinator_address: {coordinator_address}'
    )
  logging.info(
      'Using process_id %s and coordinator_address %s to initialize JAX'
      ' distributed runtime...',
      process_id,
      coordinator_address,
  )
  jax.distributed.initialize(
      process_id=int(process_id),
      coordinator_address=coordinator_address,
      initialization_timeout=jax_initialization_timeout_seconds,
  )
  return process_id

