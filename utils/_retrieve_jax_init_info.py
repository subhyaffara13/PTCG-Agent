
def _retrieve_jax_init_info(
    local_checkpoint_directory: epath.Path, *, timeout_seconds: int = 900
) -> List[str]:
  """Retrieve JAX init info from a local file.

  Args:
    local_checkpoint_directory: The local checkpoint directory.
    timeout_seconds: The timeout in seconds.

  Returns:
    A list of strings containing the JAX init info (process id and coordinator
    address).

  Raises:
    TimeoutError: if the JAX init info file is not found within the timeout.
    ValueError: if the JAX init info file is found but the values are not
    valid.

  Allow time for the JAX init info file to be populated by GKE. This is needed
  because the file is only populated when the worker with process id of 0 is
  determined. After a disruption, although some workers might be up and
  running, the init info file won't be populated until the node with process
  id of 0 is known and this could take time. Using 900 seconds for now and it
  needs to be increased if the "repair" time is longer.
  """
  local_jax_init_info_file = (
      epath.Path(local_checkpoint_directory) / _JAX_INIT_INFO_FILE
  )

  for i in range(timeout_seconds):
    if local_jax_init_info_file.exists():
      values = local_jax_init_info_file.read_text().split('\n')
      if len(values) < 2:
        raise ValueError(
            "JAX init info file doesn't have required process id and"
            f' coordinator address data: Current values: {values}'
        )
      logging.info('Found %s after %ds.', _JAX_INIT_INFO_FILE, i)
      return values[:2]
    if i % 30 == 0:
      logging.info(f'Waiting for {_JAX_INIT_INFO_FILE}... elapsed={i}s')
    time.sleep(1)
  raise TimeoutError(
      f'Unable to locate {_JAX_INIT_INFO_FILE} after {timeout_seconds} seconds,'
  )

