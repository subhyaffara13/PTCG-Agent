import logging
import math


def _construct_maximal_sharding(
    sds: jax.ShapeDtypeStruct,
    devices: Sequence[jax.Device] | None = None,
) -> jax.sharding.Sharding:
  """Constructs a sharding that partitions the array as much as possible."""
  devices = devices or jax.devices()
  device_count = len(devices)
  shape = sds.shape
  if not shape:
    return jax.sharding.NamedSharding(
        mesh=jax.sharding.Mesh(devices, ('a',)),
        spec=jax.sharding.PartitionSpec(),
    )
  if np.max(shape) < jax.device_count():
    # Array is small - no sharding needed.
    return jax.sharding.NamedSharding(
        mesh=jax.sharding.Mesh(devices, ('a',)),
        spec=jax.sharding.PartitionSpec(),
    )

  available_device_dim = device_count
  partition_axes = [None] * len(shape)
  mesh_shape = []
  mesh_axes = []

  current_partition_axis = 0
  # Max to min.
  for i in np.argsort(shape)[::-1]:
    assert available_device_dim > 0
    if available_device_dim == 1:
      break
    if shape[i] < available_device_dim:
      continue
    gcd = math.gcd(shape[i], available_device_dim)
    if gcd == 1:
      continue
    available_device_dim //= gcd
    mesh_shape.append(gcd)

    current_partition_axis_name = _partition_axis_name(current_partition_axis)
    partition_axes[i] = current_partition_axis_name
    mesh_axes.append(current_partition_axis_name)
    current_partition_axis += 1

  # Still have some partition dimension left over.
  if available_device_dim > 1:
    mesh_shape.append(available_device_dim)
    mesh_axes.append(_partition_axis_name(current_partition_axis))

  logging.info(
      'Constructed sharding for array with shape: %s, mesh_shape: %s,'
      ' mesh_axes: %s, partition_axes: %s',
      shape,
      mesh_shape,
      mesh_axes,
      partition_axes,
  )

  assert len(mesh_shape) == len(mesh_axes)
  assert len(partition_axes) == len(shape)
  mesh = jax.sharding.Mesh(
      np.asarray(devices).reshape(mesh_shape),
      tuple(mesh_axes),
  )
  pspec = jax.sharding.PartitionSpec(*partition_axes)
  return jax.sharding.NamedSharding(mesh=mesh, spec=pspec)

