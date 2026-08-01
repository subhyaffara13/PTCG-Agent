
def write_one_array(
    location: str,
    name: str,
    value: jax.Array,
    timeout: datetime.timedelta,
):
  """Creates the write array plugin program string, compiles it to an executable, calls it and returns an awaitable future."""
  write_request = get_write_request(location, name, value, timeout)
  write_executable = cloud_pathways_plugin_executable.PluginExecutable(
      write_request
  )
  _, write_future = write_executable.call([value])
  return write_future

