
def _build_transient_array(
    name: str, info: dict[str, Any], owner: int, ctx: _LoadContext
) -> jax.Array:
  """Builds transient array for general resharding case."""
  shape, dtype = _get_array_properties(info)
  num_devices_per_host = jax.local_device_count()
  if _should_replicate_array(shape):
    shard_size = None
  else:
    shard_size = shape[0] // num_devices_per_host

  np_array = None
  if ctx.host_id == owner:
    np_array = _extract_tensor_from_bundle(
        info, ctx.bundle_bytes, ctx.bundle_start_offset, shape, dtype
    )

  device_buffers = []
  for i, d in enumerate(ctx.devices_by_host[ctx.host_id]):
    if ctx.host_id == owner:
      device_buffers.append(
          _create_data_buffer(
              np_array,
              d,
              shard_size,
              i,
          )
      )
    else:
      zero_buf = ctx.zero_buffers[(d, dtype)]
      current_shard_shape = _get_current_shard_shape(shape)
      device_buffers.append(_get_zero_shard_view(zero_buf, current_shard_shape))

  abstract_transient = _get_abstract_transient_array(
      shape, dtype, ctx.global_mesh, ctx.num_hosts
  )

  try:
    return jax.make_array_from_single_device_arrays(
        abstract_transient.shape,
        abstract_transient.sharding,
        device_buffers,
    )
  except Exception as e:
    logging.error(
        "Failed make_array_from_single_device_arrays for %s: %s", name, e
    )
    raise e

