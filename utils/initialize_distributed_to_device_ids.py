import logging

def initialize_distributed_to_device_ids():
  """Initializes the device index mapping."""
  # Already initialized.
  if is_distributed_to_device_ids_initialized():
    return
  global _DISTRIBUTED_TO_DEVICE_IDS

  client = get_jax_distributed_client()
  own_distributed_id = jax._src.distributed.global_state.process_id  # pylint: disable=protected-access
  own_device_ids = [d.id for d in jax.local_devices()]
  dir_key = 'orbax/distributed_to_device_ids/'
  key = dir_key + str(own_distributed_id)
  client.key_value_set(key, str(own_device_ids))
  client.wait_at_barrier(
      # 5 minutes.
      'orbax_global_discovery_device_ids',
      timeout_in_ms=5 * 60 * 1000,
  )
  ids = client.key_value_dir_get(dir_key)
  results = [None for _ in range(jax.process_count())]
  for key, device_ids in ids:
    distributed_id = int(key.split('/')[-1])
    # Remove the list brackets.
    device_ids = device_ids[1 : len(device_ids) - 1]
    results[distributed_id] = [
        int(device_id) for device_id in device_ids.split(', ')
    ]
  assert None not in results
  _DISTRIBUTED_TO_DEVICE_IDS = results
  logging.vlog(
      1,
      '[process=%s][thread=%s] distributed_to_device_ids: %s',
      own_distributed_id,
      threading.current_thread().name,
      _DISTRIBUTED_TO_DEVICE_IDS,
  )

