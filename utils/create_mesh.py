import logging
import math


def create_mesh(config: configs.MeshConfig) -> jax.sharding.Mesh:
  """Creates a jax.sharding.Mesh from a MeshConfig object.

  Args:
      config: The MeshConfig object defining the topology.

  Returns:
      A fully configured jax.sharding.Mesh.
  """
  logging.info('Creating mesh with config: %s', config)
  devices = jax.devices()
  num_devices = len(devices)
  # Convert the user-friendly dict maps into ordered lists based on mesh_axes
  ici_shape = [config.ici_parallelism.get(axis, 1) for axis in config.mesh_axes]

  dcn_parallelism = config.dcn_parallelism
  if dcn_parallelism is None:
    logging.info('Creating ICI-only mesh.')
    devices_array = mesh_utils.create_device_mesh(ici_shape, devices)
    logging.info(
        'Creating mesh with axes: %s',
        dict(zip(config.mesh_axes, devices_array.shape)),
    )
    return jax.sharding.Mesh(devices_array, config.mesh_axes)
  else:
    logging.info('Creating hybrid mesh.')
    dcn_shape = [dcn_parallelism.get(axis, 1) for axis in config.mesh_axes]

  if jax.default_backend() == 'cpu':
    devices = jax.devices()
    # Sort devices by process index to ensure a predictable global grid
    devices = sorted(devices, key=lambda d: d.process_index)
    global_shape = tuple(d * i for d, i in zip(dcn_shape, ici_shape))
    devices_array = np.array(devices).reshape(global_shape)
    logging.info(
        'Creating CPU-only hybrid mesh with axes: %s',
        dict(zip(config.mesh_axes, devices_array.shape)),
    )
    return jax.sharding.Mesh(devices_array, config.mesh_axes)

  # --- Validation ---
  if config.process_is_granule:
    process_count = jax.process_count()
    num_devices_per_granule = num_devices // process_count
    if num_devices % process_count != 0:
      raise ValueError(
          f'Total devices ({num_devices}) must be divisible by process_count'
          f' ({process_count}).'
      )
    if np.prod(dcn_shape) != jax.process_count():
      raise ValueError(
          f'The product of DCN parallelism values {np.prod(dcn_shape)} must'
          f' equal process_count {process_count}.'
      )
  else:
    num_slices = _num_slices()
    num_devices_per_granule = num_devices // num_slices
    if num_devices % num_slices != 0:
      raise ValueError(
          f'Total devices ({num_devices}) must be divisible by num_slices'
          f' ({num_slices}).'
      )
    if np.prod(dcn_shape) != num_slices:
      raise ValueError(
          f'The product of DCN parallelism values {np.prod(dcn_shape)} must'
          f' equal num_slices {num_slices}.'
      )
  if np.prod(ici_shape) != num_devices_per_granule:
    raise ValueError(
        f'The product of ICI parallelism values {np.prod(ici_shape)} must'
        f' equal num_devices_per_granule {num_devices_per_granule}.'
    )

  # --- Mesh Creation ---
  devices_array = mesh_utils.create_hybrid_device_mesh(
      ici_shape,
      dcn_shape,
      devices,
      process_is_granule=config.process_is_granule,
      allow_split_physical_axes=config.allow_split_physical_axes,
  )
  logging.info(
      'Creating mesh with axes: %s',
      dict(zip(config.mesh_axes, devices_array.shape)),
  )
  return jax.sharding.Mesh(devices_array, config.mesh_axes)


def create_mesh(mesh_shape, axis_names, iota_order=False, axis_types=None):
  size = math.prod(mesh_shape)
  if len(xla_bridge.devices()) < size:
    raise unittest.SkipTest(f"Test requires {size} global devices and found {len(xla_bridge.devices())}.")
  if iota_order:
    devices = sorted(xla_bridge.devices(), key=lambda d: d.id)
    mesh_devices = np.array(devices[:size]).reshape(mesh_shape)
    return mesh_lib.Mesh(mesh_devices, axis_names, axis_types=axis_types)
  else:
    if axis_types is None:
      axis_types = (mesh_lib.AxisType.Auto,) * len(mesh_shape)
    return sharding_impls.make_mesh(mesh_shape, axis_names, axis_types)

