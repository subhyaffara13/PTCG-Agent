
def local_device_count(
    backend: str | xla_client.Client | None = None
) -> int:
  """Returns the number of devices addressable by this process."""
  return int(get_backend(backend).local_device_count())

