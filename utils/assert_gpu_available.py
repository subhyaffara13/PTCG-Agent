
def assert_gpu_available(backend: Optional[str] = None) -> None:
  """Checks that at least one GPU device is available.

  Args:
    backend: A type of backend to use (uses JAX default if not provided).

  Raises:
    AssertionError: If no GPU device available.
  """
  if not _ai.num_devices_available("gpu", backend=backend):
    raise AssertionError(f"No GPU devices available in {jax.devices(backend)}.")

