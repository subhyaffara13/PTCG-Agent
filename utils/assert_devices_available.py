
def assert_devices_available(n: int,
                             devtype: str,
                             backend: Optional[str] = None,
                             not_less_than: bool = False) -> None:
  """Checks that `n` devices of a given type are available.

  Args:
    n: A required number of devices of the given type.
    devtype: A type of devices, one of ``{'cpu', 'gpu', 'tpu'}``.
    backend: A type of backend to use (uses Jax default if not provided).
    not_less_than: Whether to check if the number of devices is not less than
      `n`, instead of precise comparison.

  Raises:
    AssertionError: If number of available device of a given type is not equal
                    or less than `n`.
  """
  n_available = _ai.num_devices_available(devtype, backend=backend)
  devs = jax.devices(backend)
  if not_less_than and n_available < n:
    raise AssertionError(
        f"Only {n_available} < {n} {devtype.upper()}s available in {devs}.")
  elif not not_less_than and n_available != n:
    raise AssertionError(f"No {n} {devtype.upper()}s available in {devs}.")

