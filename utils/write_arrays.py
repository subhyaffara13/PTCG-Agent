
def write_arrays(
    location: str,
    names: Sequence[str],
    values: Sequence[jax.Array],
    timeout: datetime.timedelta,
) -> concurrent.futures.Future[None]:
  """Creates the write array plugin program string, compiles it to an executable, calls it and returns an awaitable future."""
  bulk_write_request = get_bulk_write_request(location, names, values, timeout)
  bulk_write_executable = cloud_pathways_plugin_executable.PluginExecutable(
      bulk_write_request
  )
  _, bulk_write_future = bulk_write_executable.call(values)
  return bulk_write_future

