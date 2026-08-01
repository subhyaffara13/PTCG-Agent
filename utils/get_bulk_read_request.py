
def get_bulk_read_request(
    location_path: str,
    names: Sequence[str],
    dtypes: Sequence[np.dtype],
    shapes: Sequence[Sequence[int]],
    shardings: Sequence[jax.sharding.Sharding],
    devices: Sequence[jax.Device],
    timeout: datetime.timedelta,
) -> str:
  """Returns a string representation of a bulk read request, reads multiple arrays with one call."""
  read_requests = [
      get_read_request(
          location_path, name, dtype, shape, sharding, devices, timeout, True
      )["persistenceReadRequest"]
      for name, dtype, shape, sharding in zip(names, dtypes, shapes, shardings)
  ]
  return json.dumps(
      {"bulk_persistence_read_request": {"read_requests": read_requests}}
  )

