
def _globalize_single_replica_arrays(
    inp: jax.Array,
    replica_axis_index: int,
    global_mesh: jax.sharding.Mesh,
    is_source: bool,
) -> jax.Array:
  """Globalizes a single replica array."""

  num_replicas = global_mesh.devices.shape[replica_axis_index]
  replica_axis_name = global_mesh.axis_names[replica_axis_index]
  sharding = inp.sharding
  if not isinstance(sharding, jax.sharding.NamedSharding):
    raise ValueError(
        'Must provide input arrays with NamedSharding. '
        f'Got {type(sharding)} instead.'
    )
  local_replica_shape = inp.shape

  assert replica_axis_name not in sharding.spec, (
      f'Replica axis name {replica_axis_name} already exists in'
      f' sharding.spec {sharding.spec}'
  )
  global_shape = (num_replicas,) + local_replica_shape
  logging.vlog(
      1,
      'Globalizing array with local shape %s to Global shape: %s',
      local_replica_shape,
      global_shape,
  )
  global_spec = jax.sharding.PartitionSpec(
      replica_axis_name,
      *sharding.spec,
  )
  global_sharding = jax.sharding.NamedSharding(global_mesh, global_spec)

  source_device_map = {}

  if is_source:
    for s in inp.addressable_shards:
      sd_mesh = jax.sharding.Mesh(np.array([s.device]), ('_single',))
      if hasattr(jax, 'set_mesh'):
        with jax.set_mesh(sd_mesh):
          source_device_map[s.device] = jnp.expand_dims(s.data, axis=0)
      else:
        with sd_mesh:
          source_device_map[s.device] = jnp.expand_dims(s.data, axis=0)

  device_buffers = []
  for d, index in global_sharding.addressable_devices_indices_map(
      global_shape
  ).items():
    if d in source_device_map:
      device_buffers.append(source_device_map[d])
    else:
      # Use jax.numpy.zeros to allocate directly on device
      # to avoid Host RAM spike.
      slice_shape = _get_slice_shape(index, global_shape)
      sd_mesh = jax.sharding.Mesh(np.array([d]), ('_single',))
      if hasattr(jax, 'set_mesh'):
        with jax.set_mesh(sd_mesh):
          zero_data = jnp.zeros(slice_shape, dtype=inp.dtype, device=d)
      else:
        with sd_mesh:
          zero_data = jnp.zeros(slice_shape, dtype=inp.dtype, device=d)
      device_buffers.append(zero_data)

  logging.vlog(
      1,
      'Device buffers: %r',
      {d.device: d for d in device_buffers},
  )
  return jax.make_array_from_single_device_arrays(
      global_shape,
      global_sharding,
      device_buffers,
      dtype=inp.dtype,
  )

