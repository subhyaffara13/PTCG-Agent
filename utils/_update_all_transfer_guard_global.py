
def _update_all_transfer_guard_global(val):
  for name in ('jax_transfer_guard_host_to_device',
               'jax_transfer_guard_device_to_device',
               'jax_transfer_guard_device_to_host'):
    config.update(name, val)

