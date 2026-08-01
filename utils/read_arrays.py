
def read_arrays(
    location: str,
    names: Sequence[str],
    dtypes: Sequence[np.dtype],
    shapes: Sequence[Sequence[int]],
    shardings: Sequence[jax.sharding.Sharding],
    devices: Sequence[jax.Device] | np.ndarray,
    timeout: datetime.timedelta,
) -> tuple[Sequence[jax.Array], concurrent.futures.Future[None]]:
  """Creates the read array plugin program string, compiles it to an executable, calls it and returns the result."""

  bulk_read_request = get_bulk_read_request(
      location, names, dtypes, shapes, shardings, devices, timeout
  )
  bulk_read_executable = cloud_pathways_plugin_executable.PluginExecutable(
      bulk_read_request
  )
  out_avals = [
      core.ShapedArray(shape, dtype) for shape, dtype in zip(shapes, dtypes)
  ]
  arrays, read_future = bulk_read_executable.call(
      out_shardings=shardings, out_avals=out_avals
  )
  return (arrays, read_future)

