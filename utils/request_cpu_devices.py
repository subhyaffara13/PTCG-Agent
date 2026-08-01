
def request_cpu_devices(nr_devices: int):
  """Requests at least `nr_devices` CPU devices.

  request_cpu_devices should be called at the top-level of a test module before
  main() runs.

  It is not guaranteed that the number of CPU devices will be exactly
  `nr_devices`: it may be more or less, depending on how exactly the test is
  invoked. Test cases that require a specific number of devices should skip
  themselves if that number is not met.
  """
  if xla_bridge.num_cpu_devices.value < nr_devices:
    xla_bridge.get_backend.cache_clear()
    # Don't raise an error for `request_cpu_devices` because we initialize the
    # backend in OSS during collecting tests in pytest via `device_under_test`.
    try:
      config.update("jax_num_cpu_devices", nr_devices)
    except RuntimeError:
      pass

