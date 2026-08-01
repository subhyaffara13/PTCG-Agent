
def save_device_memory_profile(filename, backend: str | None = None) -> None:
  """Collects a device memory profile and writes it to a file.

  :func:`save_device_memory_profile` is a convenience wrapper around :func:`device_memory_profile`
  that saves its output to a ``filename``. See the
  :func:`device_memory_profile` documentation for more information.

  Args:
    filename: the filename to which the profile should be written.
    backend: optional; the name of the JAX backend for which the device memory
      profile should be collected.
  """
  profile = device_memory_profile(backend)
  with open(filename, "wb") as f:
    f.write(profile)

