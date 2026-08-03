import logging

def initialize_runtime_to_distributed_ids():
  """Initializes the process index mapping.

  Note that this function is for experimental purposes only. It is intended to
  be called exactly once per processes.

  TODO(b/325293150): Remove once the bug is resolved.
  """
  global _RUNTIME_TO_DISTRIBUTED_ID
  client = get_jax_distributed_client()

  # Index is distributed id.
  # Value is runtime id.
  _RUNTIME_TO_DISTRIBUTED_ID = [0 for _ in range(jax.process_count())]
  own_runtime_id = jax.process_index()
  own_distributed_id = jax._src.distributed.global_state.process_id  # pylint: disable=protected-access
  dir_key = 'jax/process_id/'
  key = dir_key + str(own_runtime_id)
  client.key_value_set(key, str(own_distributed_id))
  client.wait_at_barrier('orbax_global_discovery', timeout_in_ms=5 * 60 * 1000)
  ids = client.key_value_dir_get(dir_key)
  for key, distributed_id in ids:
    runtime_id = int(key.split('/')[-1])
    _RUNTIME_TO_DISTRIBUTED_ID[runtime_id] = int(distributed_id)
  logging.vlog(
      1,
      '[process=%s][thread=%s] runtime_to_distributed_id: %s',
      process_index(),
      threading.current_thread().name,
      _RUNTIME_TO_DISTRIBUTED_ID,
  )

