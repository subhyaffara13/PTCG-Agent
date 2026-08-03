from typing import Optional

def assert_tpu_available(backend: Optional[str] = None) -> None:
  """Checks that at least one TPU device is available.

  Args:
    backend: A type of backend to use (uses JAX default if not provided).

  Raises:
    AssertionError: If no TPU device available.
  """
  if not _ai.num_devices_available("tpu", backend=backend):
    raise AssertionError(f"No TPU devices available in {jax.devices(backend)}.")

