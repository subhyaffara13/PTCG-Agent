
def is_single_process_multi_device_topology():
  return (jax.device_count() > 1
          and jax.device_count() == jax.local_device_count())

