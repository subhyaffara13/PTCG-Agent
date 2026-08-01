
def get_bulk_write_request(
    location_path: str,
    names: Sequence[str],
    jax_arrays: Sequence[jax.Array],
    timeout: datetime.timedelta,
) -> str:
  """Returns a string representation of a bulk write request, writes multiple arrays with one call."""
  write_requests = [
      get_write_request(location_path, name, jax_array, timeout, True)[
          "persistenceWriteRequest"
      ]
      for name, jax_array in zip(names, jax_arrays)
  ]
  return json.dumps(
      {"bulk_persistence_write_request": {"write_requests": write_requests}}
  )

