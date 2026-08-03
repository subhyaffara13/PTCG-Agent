from typing import List

def runtime_to_distributed_ids() -> List[int]:
  if not is_runtime_to_distributed_ids_initialized():
    raise ValueError('Please call initialize_runtime_to_distributed_ids().')
  return _RUNTIME_TO_DISTRIBUTED_ID


def runtime_to_distributed_ids() -> List[int]:
  """Returns the runtime to distributed process id mapping."""
  # TODO(b/325293150): Deprecate this after jaxlib contains the fix.
  result = multihost.runtime_to_distributed_ids()
  runtime_and_distributed_ids_are_the_same = all([
      result[i] == i for i in range(len(result))
  ])

  # JAX may choose to overwrite the device process index with the distributed
  # process index. In that case, we have to use the device id to infer the real
  # device process index. This is a hack, the intent is to remove it once this
  # workaround is no longer needed.
  if runtime_and_distributed_ids_are_the_same:
    result = [-1 for _ in range(jax.process_count())]
    devices = jax.devices()
    for i in range(0, jax.device_count(), jax.local_device_count()):
      result[process_index_from_device_id(devices[i].id)] = devices[
          i
      ].process_index
    assert -1 not in result
  return result

